"""
GEO-SRA Downloader
===================
Placeholder.

Authors: Eduardo G. Gusmao.

"""

###################################################################################################
# Libraries
###################################################################################################

# Python
import os
import time
import glob
import gzip
import shutil
import requests
import functools
import subprocess
import multiprocessing
from pathlib import Path
from typing import Optional, Dict, List

# Internal


# External
import GEOparse
import pandas as pd
from Bio import Entrez
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

###################################################################################################
# Constants
###################################################################################################

# import GEOparse.GEOparse as geo_parser

# def get_GEO_file_http(geo):
#     """Force GEOparse to use HTTPS instead of FTP."""
#     return f"https://ftp.ncbi.nlm.nih.gov/geo/series/{geo[:-3]}nnn/{geo}/soft/{geo}_family.soft.gz"

# # Monkey-patch the function
# geo_parser.get_GEO_file = get_GEO_file_http

# Path to your manually installed Chromium + Chromedriver
CHROME_BIN = "/home/egusmao/.opt/chromium/chrome-linux64/chrome"
CHROMEDRIVER_BIN = "/home/egusmao/.opt/chromium_driver/chromedriver-linux64/chromedriver"

# Fixed file name suffix
TEMP_SUFFIX = "_temp"
METADATA_SUFFIX = "_metadata.tsv"
STUDY_SUFFIX = "_study.tsv"

###################################################################################################
# Classes
###################################################################################################

class GEODataDownloader:
    """
    A class for downloading data from GEO, including processed files, raw SRA files, 
    and associated metadata.

    Supports:
    - Processed data files from GEO Series (GSE) and Samples (GSM).
    - Raw sequencing data from SRA (via 'fastq-dump').
    - Automatic parsing of metadata to label and organize files correctly.

    Attributes
    ----------
    geo_id : str
        The GEO or SRA accession ID (e.g., "GSE12345", "SRP09876").
    output_dir : Path
        Directory where downloaded files will be stored.
    _temp_file_name : Path
        Temporary directory to store metadata and intermediate files.
    _gse : GEOparse.GSE
        GEO Series object for metadata extraction.
    """

    def __init__(self,
                 geo_id: str,
                 output_dir: str = "data/raw",
                 email: str = None,
                 api_key: str = None,
                 ncbi_dir: str = None):
        """
        Initialize the downloader.

        Parameters
        ----------
        geo_id : str
            The GEO or SRA accession ID (e.g., "GSE12345", "SRP09876").
        output_dir : str, optional
            Directory where downloaded files will be stored, by default "data/raw".
        email : str, optional
            Email address for Entrez authentication.
        api_key : str, optional
            NCBI API key for higher rate limits.

        Raises
        ------
        ValueError
            Invalid email provided to set NCBI Entrez credentials.
        """

        # GEO ID
        self.geo_id = geo_id
        self.metadata_table = None # Metadata Table
        self._gse = None # GEO Series object
        self._temp_file_name = None # Temporary location to store indermediary files

        # Output directory processing
        self.output_dir = Path(output_dir) / f"{self.geo_id}"
        self.output_dir.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

        # NCBI directory processing
        if ncbi_dir is not None:
            self.ncbi_dir = Path(ncbi_dir) / f"sra"
            self.ncbi_dir.mkdir(parents=True, exist_ok=True)

        # Set credentials for NCBI Entrez API
        if email is not None and api_key is not None:
            Entrez.email = self.email = email
            Entrez.api_key = self.api_key = api_key

        # Fetch metadata
        metadata_table = self.output_dir / f"{self.geo_id}{METADATA_SUFFIX}"
        # If metadata_table exists, do not create all the metadata structure
        if metadata_table.exists():
            self.metadata_table = metadata_table
        # Fetch metadata first, as it is required before downloading any data
        else:
            if self._is_gse():
                # Temporary directory for storing metadata and intermediate files
                self._temp_file_name = self.output_dir / f"{self.geo_id}{TEMP_SUFFIX}"
                self._temp_file_name.mkdir(parents=True, exist_ok=True)

                # Fetch GEO metadata
                self._gse = self._fetch_gse_data()

                # Create metadata and study tables
                self.create_metadata_table()

    def __del__(self) -> None:
        """
        Destructor to clean up temporary files when the object is deleted.

        Notes
        -----
        - This method ensures that temporary metadata files are deleted 
          when the instance is garbage collected.
        - The actual downloaded data remains untouched in 'self.output_dir'.
        """
        self.cleanup()

    def create_metadata_table(self) -> None:
        """
        Extracts metadata from GEO and SRA, processes it into a structured table, 
        and saves the result as a TSV file.

        This function follows a structured pipeline:
        1. Extract study-wide metadata.
        2. Extract sample-level metadata.
        3. Map GSM (sample IDs) to SRX (experiment IDs).
        4. Fetch SRR (run IDs) corresponding to each experiment.
        5. Merge metadata into a Pandas DataFrame.
        6. Insert study-wide metadata as the first two rows.
        7. Save the final table in a tab-separated format.

        Notes
        -----
        - The first two rows of the table will contain **study-wide metadata** 
          (keys in row 1, values in row 2).
        - Sample-specific metadata follows from row 3 onward.
        - The final table will be stored at 'self.output_dir'.

        Raises
        ------
        Exception
            If there is an issue extracting metadata or writing the file.
        """
        
        # Step 1: Extract study-wide metadata (e.g., experiment details, project description)
        study_dictionary = self._extract_study_metadata()

        # Step 2: Extract sample-specific metadata (e.g., sample name, organism, molecule type)
        sample_dictionary = self._extract_sample_metadata()

        # Step 3: Extract mapping between GSM (samples) and SRX (experiments)
        gsm_to_srx = self._extract_srx_from_gse()

        # Step 4: Process GSM -> SRX -> SRR Mapping
        geo_sra_data = []  # List to store processed metadata
        for gsm, srx in gsm_to_srx.items():
            srr_ids = self._fetch_srr_from_srx(srx)  # Fetch run IDs for the experiment
            time.sleep(2)  # Delay to prevent rate limits from SRA servers

            # Step 4.1: Merge metadata with SRX and SRR information
            merged_data = sample_dictionary.get(gsm, {}).copy()  # Retrieve sample metadata
            merged_data.update({
                "GSM_ID": gsm,  # GEO Sample ID
                "SRX_ID": srx,  # SRA Experiment ID
                "SRR_IDs": ",".join(srr_ids) if srr_ids else "No SRRs found"  # List of run IDs
            })

            geo_sra_data.append(merged_data)

        # Step 5: Convert collected data into a Pandas DataFrame
        df_samples = pd.DataFrame(geo_sra_data)

        # Step 6: Convert study-wide metadata into a DataFrame (first row: keys, second row: values)
        df_study = pd.DataFrame([study_dictionary])

        # Step 7: Save the final study table as a TSV file
        study_out_path = self.output_dir / f"{self.geo_id}{STUDY_SUFFIX}"
        df_study.to_csv(study_out_path, sep="\t", index=False)

        # Step 8: Save the final metadata table as a TSV file
        metadata_out_path = self.output_dir / f"{self.geo_id}{METADATA_SUFFIX}"
        df_samples.to_csv(metadata_out_path, sep="\t", index=False)
        self.metadata_table = Path(metadata_out_path).resolve()

    def download_raw_data(self) -> None:
        """
        Downloads raw sequencing data (FASTQ files) from SRA using 'prefetch'.

        This method reads the previously generated metadata table (TSV), extracts
        all **SRR** (SRA Run IDs), and downloads the corresponding sequencing data.

        Workflow:
        1. Open the metadata table generated by 'create_metadata_table()'.
        2. Extract all SRR (SRA Run IDs) from the metadata.
        3. Create log file locations and append SRR into a list.
        4. Use 'prefetch' (from SRA Toolkit) to download FASTQ files.

        Parameters
        ----------
        Future : Pass prefetch parameters

        Raises
        ------
        FileNotFoundError
            If the metadata file does not exist.
        ValueError
            If the metadata file is missing the 'SRR_IDs' column.
        """

        # Step 1: Initialize metadata and check wether the file exists
        metadata_file = self.output_dir / f"{self.geo_id}_metadata.tsv"
        if not metadata_file.exists():
            raise FileNotFoundError(f"Metadata table not found: {metadata_file}")

        # Step 1: Fetch metadata from file
        metadata_df = pd.read_csv(metadata_file, sep="\t")
        if "SRR_IDs" not in metadata_df.columns:
            raise ValueError("Metadata table is missing 'SRR_IDs' column!")

        # Step 2: Fetch SRRs from metadata
        sra_id_list = []
        for _, row in metadata_df.iterrows():
            srr_list = str(row["SRR_IDs"]).split(",")

            # Iterate on SRR list
            for sra_id in srr_list:
                sra_id = sra_id.strip()

                # Check SRR validity
                if sra_id.lower() in ["no srrs found", "nan", ""]:
                    print(f"No SRRs found for {row['GSM_ID']} (Skipping)")
                    continue

                # Checking whether sra files already exist
                sra_file = self.ncbi_dir / f"{sra_id}.sra"
                sra_file_lite = self.ncbi_dir / f"{sra_id}.sralite"
                if sra_file.exists() or sra_file_lite.exists():
                    print(f"{sra_id} already exists, skipping conversion.")
                    continue

                # Step 3: Create log file
                log_file = self.output_dir / f"prefetch_{sra_id}.log"

                # Step 3: SRA is AWS-only
                if self._get_sra_aws_links(sra_id):
                    continue

                # Step 3: Append ssr_id and log_file to list
                else:
                    print(f"SRA = {sra_id} is available via NCBI. Using prefetch.")
                    sra_id_list.append((sra_id, log_file))

        # Step 4: Run '_download_with_prefetch' function
        for sra_id, log_file in sra_id_list:
            self._download_with_prefetch(sra_id,
                                         max_size_gb="500G",
                                         log_level="6",
                                         log_file=log_file)

        print("\n All SRA runs downloaded to the default location.")

    def process_sra_to_fastq(self, num_workers: int = None) -> None:
        """
        Convert SRA (raw sequencing data) into FASTQ files using 'fastq-dump'.

        This method reads the previously generated metadata table (TSV), extracts
        all **SRR** (SRA Run IDs), and converts the corresponding sequencing data.

        Workflow:
        1. Open the metadata table generated by 'create_metadata_table()'.
        2. Create a 'GSEXXXXXX' subfolder inside 'self.output_dir' for storing fastq files.
        3. Extract all SRR (SRA Run IDs) from the metadata.
        4. Set the stage for multiprocessing function's Pool.
        5. Use 'fastq-dump' (from SRA Toolkit) to convert SRA to FASTQ files.

        Parameters
        ----------
        num_workers : int
            Number of cores or processing units to parallelize.

        Raises
        ------
        FileNotFoundError
            If the metadata file does not exist.
        ValueError
            If the metadata file is missing the 'SRR_IDs' column.
        """

        # Step 1: Initialize metadata and check wether the file exists
        metadata_file = self.output_dir / f"{self.geo_id}_metadata.tsv"
        if not metadata_file.exists():
            raise FileNotFoundError(f"Metadata table not found: {metadata_file}")

        # Step 1: Fetch metadata from file
        metadata_df = pd.read_csv(metadata_file, sep="\t")
        if "SRR_IDs" not in metadata_df.columns:
            raise ValueError("Metadata table is missing 'SRR_IDs' column!")

        # Step 2: Initialize final output firectory and creates if it does not exist already
        final_output_dir = self.output_dir
        final_output_dir.mkdir(parents=True, exist_ok=True)

        # Step 3: Fetch SRRs from metadata
        sra_id_list = []
        for _, row in metadata_df.iterrows():
            srr_list = str(row["SRR_IDs"]).split(",")

            # Iterate on SRR list
            for sra_id in srr_list:
                sra_id = sra_id.strip()

                # Check SRR validity
                if sra_id.lower() in ["no srrs found", "nan", ""]:
                    print(f"No SRRs found for {row['GSM_ID']} (Skipping)")
                    continue

                # Checking whether fastq files already exist
                fastq_file_list = [
                    final_output_dir / f"{sra_id}.fastq.gz",
                    final_output_dir / f"{sra_id}_1.fastq.gz",
                    final_output_dir / f"{sra_id}_2.fastq.gz",
                    final_output_dir / f"{sra_id}_R1.fastq.gz",
                    final_output_dir / f"{sra_id}_R2.fastq.gz",
                    final_output_dir / f"{sra_id}_R3.fastq.gz",
                    final_output_dir / f"{sra_id}_I2.fastq.gz",
                    final_output_dir / f"{sra_id}_I5.fastq.gz",
                ]
                cont_flag = False
                for fastq_file_name in fastq_file_list:
                    if fastq_file.exists():
                        print(f"{fastq_file_name} already exists, skipping.")
                        cont_flag = True
                        continue
                if cont_flag:
                    continue

                # Step 3: Append ssr_id to list
                sra_id_list.append(sra_id)

        # Step 4: Setting the number of CPUs
        if num_workers is None:
            # Use half of available CPUs, but no more than 10 (NCBI's limit)
            num_workers = min(max(1, int(ceil(os.cpu_count() / 2))),10)

        # Step 4: Partial parameter encapsulation for '_process_sra_to_fastq'
        convert_partial = functools.partial(
            self._process_sra_to_fastq,
            log_level = "5",
            gzip_files=True,
            split_files=False,
            split_3=True,
            output_directory = final_output_dir,
        )

        # Step 5: Apply '_process_sra_to_fastq' using multiprocessing
        with multiprocessing.Pool(processes=num_workers) as pool:
            pool.map(convert_partial, sra_id_list)

    def get_prefetch_sra_id_list(self, check_fastq_exists=False, check_prefetch_exists=False) -> List:
        """
        Get a list with all the SRA IDs.

        Raises
        ------
        Placeholder
        """

        # Initialize metadata and check wether the file exists
        metadata_file = self.output_dir / f"{self.geo_id}_metadata.tsv"
        if not metadata_file.exists():
            print(f"Metadata table not found: {metadata_file}")
            return None

        # Fetch metadata from file
        metadata_df = pd.read_csv(metadata_file, sep="\t")
        if "SRR_IDs" not in metadata_df.columns:
            print("Metadata table is missing 'SRR_IDs' column!")
            return None

        # Fetch SRRs from metadata
        final_output_dir = self.output_dir
        final_output_dir = Path(final_output_dir).resolve()
        sra_id_list = []
        for _, row in metadata_df.iterrows():
            srr_list = str(row["SRR_IDs"]).split(",")

            # Iterate on SRR list
            for sra_id in srr_list:
                sra_id = sra_id.strip()

                # Check SRR validity
                if sra_id.lower() in ["no srrs found", "nan", ""]:
                    print(f"No SRRs found for {row['GSM_ID']} (Skipping)")
                    continue

                # Checking whether fastq files already exist
                if check_fastq_exists:
                    fastq_file_list = [
                        final_output_dir / f"{sra_id}.fastq.gz",
                        final_output_dir / f"{sra_id}_1.fastq.gz",
                        final_output_dir / f"{sra_id}_2.fastq.gz",
                        final_output_dir / f"{sra_id}_R1.fastq.gz",
                        final_output_dir / f"{sra_id}_R2.fastq.gz",
                        final_output_dir / f"{sra_id}_R3.fastq.gz",
                        final_output_dir / f"{sra_id}_I2.fastq.gz",
                        final_output_dir / f"{sra_id}_I5.fastq.gz",
                    ]
                    cont_flag = False
                    for fastq_file_name in fastq_file_list:
                        if fastq_file_name.exists():
                            print(f"{fastq_file_name} already exists, skipping.")
                            cont_flag = True
                            continue
                    if cont_flag:
                        continue

                # Check if prefetch file exists
                prefetch_exist_flag = True
                if check_prefetch_exists:
                    prefetch_exist_flag = False
                    prefetch_file = self.ncbi_dir / f"{sra_id}.sra"
                    prefetch_file_lite = self.ncbi_dir / f"{sra_id}.sralite"
                    if prefetch_file.exists() or prefetch_file_lite.exists():
                        prefetch_exist_flag = True

                if prefetch_exist_flag:        
                    sra_id_list.append(sra_id)

        return sra_id_list

    def download_processed_data(self) -> None:
        """
        Downloads processed data files (e.g., counts, expression matrices) from GEO.

        GEO provides processed data as supplementary files, accessible via FTP.

        Workflow:
        1. Construct the GEO FTP URL based on the GEO ID format.
        2. Fetch the list of available processed files.
        3. Download each file and save it in 'self.output_dir/Processed'.
        4. Handle missing files and failed downloads gracefully.

        Raises
        ------
        ValueError
            If the GEO ID is invalid.
        RuntimeError
            If file download fails.
        """

        # Step 1: Construct base GEO FTP URL
        GEO_BASE_URL = "https://ftp.ncbi.nlm.nih.gov/geo/"
        
        if self.geo_id.startswith("GSE"):
            url = f"{GEO_BASE_URL}series/{self.geo_id[:-3]}nnn/{self.geo_id}/suppl/"
        elif self.geo_id.startswith("GSM"):
            url = f"{GEO_BASE_URL}samples/{self.geo_id[:-3]}nnn/{self.geo_id}/suppl/"
        else:
            raise ValueError("Invalid GEO ID format. Expected GSExxxx or GSMxxxx.")

        print(f"Checking for processed data files at: {url}")

        # Step 2: Fetch list of available files (assumes '_fetch_file_list' is implemented)
        file_list = self._fetch_file_list(url)

        if not file_list:
            print("No processed data files found.")
            return

        # Step 3: Create output directory for processed data
        processed_output_dir = self.output_dir / "interim"
        processed_output_dir.mkdir(parents=True, exist_ok=True)

        # Step 4: Download each file
        for filename in file_list:
            file_url = url + filename
            output_path = processed_output_dir / filename

            if output_path.exists():
                print(f"{filename} already exists, skipping download.")
                continue

            print(f"Downloading {filename}...")
            try:
                response = requests.get(file_url, stream=True)
                response.raise_for_status()  # Raise error if request failed
                
                with open(output_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                print(f"Downloaded: {filename}")

            except requests.RequestException:
                print(f"Failed to download {filename}.")
                continue  # Skip failed downloads

        print(f"\nAll processed data downloaded to: {processed_output_dir}")

    def _is_gse(self) -> bool:
        """
        Check if the provided GEO ID corresponds to a GEO Series (GSE).

        Returns
        -------
        bool
            True if the ID is a GSE accession, False otherwise.
        """
        return self.geo_id.startswith("GSE")  # Simple check for GEO Series IDs

    def _fetch_gse_data(self) -> GEOparse.GSE:
        """
        Fetches GEO Series data for a given GEO accession ID (GSE).

        This method downloads metadata and associated files from the NCBI GEO database.
        If the data is already downloaded in the temporary directory, it will reuse it.

        Returns
        -------
        GEOparse.GEO.GSE
            A GEOparse GSE object containing dataset metadata and sample information.

        Raises
        ------
        ValueError
            If the GEO ID does not start with 'GSE'.
        RuntimeError
            If downloading or parsing the GEO dataset fails.

        Examples
        --------
        >>> gse = self._fetch_gse_data()
        >>> print(gse.metadata["title"])
        """

        # Ensure GEO ID is valid
        if not self.geo_id.startswith("GSE"):
            raise ValueError("Invalid GEO ID. This function only supports GSE IDs.")

        print(f"Fetching GEO dataset: {self.geo_id}")

        try:
            # Fetch GEO dataset, storing it in a temporary directory
            gse = GEOparse.get_GEO(geo=self.geo_id, destdir=str(self._temp_file_name))

            print(f"Successfully fetched GEO dataset: {self.geo_id}")
            return gse

        except Exception as e:
            raise RuntimeError(f"Failed to fetch GEO dataset {self.geo_id}: {e}")

    def _extract_study_metadata(self) -> Dict[str, str]:
        """
        Extracts study-wide metadata from the GEO dataset.

        This method retrieves general study information, such as the dataset title, 
        summary, and experimental design.

        Returns
        -------
        Dict[str, str]
            A dictionary containing the study-wide metadata.

        Raises
        ------
        AttributeError
            If '_gse' is not initialized or contains invalid metadata.

        Examples
        --------
        >>> study_metadata = self._extract_study_metadata()
        >>> print(study_metadata["Dataset Title"])
        """

        if not self._gse:
            raise AttributeError("GEO dataset not loaded. Call '_fetch_gse_data()' first.")

        try:
            study_metadata = {
                "Dataset Title": "; ".join(self._gse.metadata.get("title", [])),
                "Dataset Summary": "; ".join(self._gse.metadata.get("summary", [])),
                "Dataset Design": "; ".join(self._gse.metadata.get("overall_design", []))
            }
        except KeyError as e:
            raise KeyError(f"Metadata key missing: {e}")

        return study_metadata

    def _extract_sample_metadata(self) -> Dict[str, Dict[str, str]]:
        """
        Extracts metadata for each sample (GSM) in the GEO dataset.

        This method iterates through all samples, extracting relevant details such as
        the sample title, organism, library strategy, and experimental conditions.

        Returns
        -------
        Dict[str, Dict[str, str]]
            A dictionary where each key is a **Sample ID (GSM_ID)**, and the value 
            is another dictionary containing the metadata fields.

        Raises
        ------
        AttributeError
            If '_gse' is not initialized or contains invalid metadata.

        Examples
        --------
        >>> sample_metadata = self._extract_sample_metadata()
        >>> print(sample_metadata["GSM123456"]["Title"])
        """

        if not self._gse:
            raise AttributeError("GEO dataset not loaded. Call '_fetch_gse_data()' first.")

        sample_dict = {}

        for sample_id, sample in self._gse.gsms.items():
            try:
                metadata = {
                    "Sample_ID": sample_id,
                    "Title": "; ".join(sample.metadata.get("title", [])),
                    "Source_Name": "; ".join(sample.metadata.get("source_name_ch1", [])),
                    "Organism": "; ".join(sample.metadata.get("organism_ch1", [])),
                    "Molecule": "; ".join(sample.metadata.get("molecule_ch1", [])),
                    "Characteristics": "; ".join(sample.metadata.get("characteristics_ch1", [])),
                    "Library_Source": "; ".join(sample.metadata.get("library_source", [])),
                    "Library_Strategy": "; ".join(sample.metadata.get("library_strategy", [])),
                    "Description": "; ".join(sample.metadata.get("description", []))
                }

                sample_dict[sample_id] = metadata

            except Exception as e:
                print(f"Error processing sample {sample_id}: {e}")
                continue  # Skip problematic samples

        return sample_dict

    def _extract_srx_from_gse(self) -> Dict[str, str]:
        """
        Extracts **SRA Experiment IDs (SRX)** from GSM metadata.

        This method scans the metadata of all samples (GSMs) and identifies 
        SRA links, extracting the corresponding **SRX IDs**.

        Returns
        -------
        Dict[str, str]
            A dictionary mapping **GSM_IDs** (keys) to their corresponding **SRX_IDs** (values).
            If no SRX is found for a given GSM, it will not be included in the dictionary.

        Raises
        ------
        AttributeError
            If '_gse' is not initialized or does not contain sample metadata.

        Examples
        --------
        >>> srx_mapping = self._extract_srx_from_gse()
        >>> print(srx_mapping["GSM123456"])  # Expected Output: "SRX123456"
        """

        if not self._gse:
            raise AttributeError("GEO dataset not loaded. Call '_fetch_gse_data()' first.")

        srx_mapping = {}

        for gsm_id, gsm in self._gse.gsms.items():
            relations = gsm.metadata.get("relation", [])

            for relation in relations:
                if "SRA:" in relation:
                    srx_id = relation.split("SRA:")[-1].strip()

                    # Extract SRX ID from full NCBI link if present
                    if "https://www.ncbi.nlm.nih.gov/sra?term=" in srx_id:
                        srx_id = srx_id.split("term=")[-1]

                    # Ensure valid SRX ID before storing
                    if srx_id.startswith("SRX"):
                        srx_mapping[gsm_id] = srx_id

        if not srx_mapping:
            print("Warning: No SRX IDs were found in the dataset.")

        return srx_mapping

    def _fetch_srr_from_srx(self, srx_id: str) -> List[str]:
        """
        Queries **NCBI SRA** for **SRR (Run IDs)** using the given **SRX Experiment ID**.

        This method performs an HTTP request to the **NCBI SRA database** and extracts all
        associated **SRR run IDs**, which are required for downloading sequencing data.

        Parameters
        ----------
        srx_id : str
            The **SRX Experiment ID** for which **SRR IDs** should be retrieved.

        Returns
        -------
        List[str]
            A list of **SRR run IDs** associated with the provided SRX ID.
            Returns an empty list if no SRRs are found.

        Raises
        ------
        ValueError
            If an invalid or empty SRX ID is provided.
        requests.RequestException
            If the HTTP request to NCBI fails.

        Examples
        --------
        >>> srr_list = self._fetch_srr_from_srx("SRX123456")
        >>> print(srr_list)  # Expected Output: ["SRR987654", "SRR987655"]
        """

        if not srx_id or not srx_id.startswith("SRX"):
            raise ValueError(f"Invalid SRX ID provided: {srx_id}")

        url = f"https://www.ncbi.nlm.nih.gov/sra/?term={srx_id}"
        print(f"Fetching SRR IDs for {srx_id}...")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        except requests.RequestException as e:
            print(f"Failed to fetch SRX {srx_id}: {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        srr_list = []

        # Search for SRR links in the HTML response
        for link in soup.find_all("a"):
            text = link.text.strip()
            if text.startswith("SRR"):
                srr_list.append(text)

        if not srr_list:
            print(f"Warning: No SRR IDs found for {srx_id}")

        return srr_list

    def _download_with_prefetch(self,
                                sra_id: str,
                                type: str = "", # Default
                                transport: str = "", # Default
                                min_size_kb: str = "", # Default
                                max_size_gb: str = "250G",
                                resume: str = "", # Default
                                verify: str = "yes", # Default
                                output_file: str = "", # Default (RECOMMENDED)
                                output_directory: str = "", # Default (RECOMMENDED)
                                log_level: str = "6",
                                verbose: str = True, # Default
                                quiet: str = False, # Default
                                log_file: str = "prefetch.log") -> None:
        """
        Download an SRA/SRR file with prefetch.

        Usage:
          prefetch [options] <SRA accession> [...]
          Download SRA files and their dependencies

        Options:
          -T|--type <value>                Specify file type to download. Default: sra 
          -t|--transport <http|fasp|both>  Transport: one of: fasp; http; both 
                                           [default]. (fasp only; http only; first try 
                                           fasp (ascp), use http if cannot download 
                                           using fasp). 
          -N|--min-size <size>             Minimum file size to download in KB 
                                           (inclusive). 
          -X|--max-size <size>             Maximum file size to download in KB 
                                           (exclusive). Default: 20G 
          -r|--resume <yes|no>             Resume partial downloads: one of: no, yes 
                                           [default].
          -C|--verify <yes|no>             Verify after download: one of: no, yes 
                                           [default].
          -o|--output-file <FILE>          Write file to FILE when downloading 
                                           single file. 
          -O|--output-directory <DIRECTORY>  Save files to DIRECTORY/ 

          -L|--log-level <level>           Logging level as number or enum string. One 
                                           of (fatal|sys|int|err|warn|info|debug) or 
                                           (0-6) Current/default is warn. 
          -v|--verbose                     Increase the verbosity of the program 
                                           status messages. Use multiple times for more 
                                           verbosity. Negates quiet. 
          -q|--quiet                       Turn off all status messages for the 
                                           program. Negated by verbose.


        This method runs 'fastq-dump' with configurable options to download 
        and convert raw sequencing data from **NCBI SRA** into FASTQ format.

        Parameters
        ----------
        sra_id : str
            The **SRA Run accession ID** (e.g., "SRR123456").
        split_files : bool, optional
            Whether to split paired-end reads into '_1.fastq' and '_2.fastq' files. Default is False.
        split_3 : bool, optional
            Whether to split three reads (forward, reverse, and index/barcode) into separate files.
            If 'split_files=True', this is ignored. Default is True.
        gzip_files : bool, optional
            Whether to compress the FASTQ output using gzip ('.fastq.gz'). Default is True.
        log_file : str, optional
            Path to the log file (default: "{sra_id}.log").

        Raises
        ------
        ValueError
            If 'sra_id' is empty or not a valid SRA accession.
        FileNotFoundError
            If 'fastq-dump' is not installed or not found in the system path.
        subprocess.CalledProcessError
            If 'fastq-dump' execution fails (e.g., due to network issues or NCBI restrictions).


        Examples
        --------
        >>> downloader._download_with_fastq_dump("SRR123456")
        Running fastq-dump for SRR123456...
        Finished fastq-dump for SRR123456

        >>> downloader._download_with_fastq_dump("SRR789012", split_files=True, gzip_files=False)
        Running fastq-dump for SRR789012...
        Finished fastq-dump for SRR789012

        Notes
        -----
        - Future implementations include adding Kart support.
        """

        # Check SRA ID
        if not sra_id or not sra_id.startswith("SRR"):
            raise ValueError(f"Invalid SRA ID provided: {sra_id}")

        print(f"Running prefetch for {sra_id}..." + "-"*30)

        # Ensure output directory exists
        if output_directory:
            out_dir = Path(output_directory)
            out_dir.mkdir(parents=True, exist_ok=True)

        # Define prefetch parameters using a dictionary
        prefetch_params = {
            "--type": type,
            "--transport": transport,
            "--min-size": min_size_kb,
            "--max-size": max_size_gb,
            "--resume": resume,
            "--verify": verify,
            "--output-file": output_file,
            "--output-directory": output_directory,
            "--log-level": log_level,
            "--verbose": verbose,
            "--quiet": quiet,
        }

        # Convert dictionary into a cleaned list of CLI arguments
        optional_parameters = []
        for key, value in prefetch_params.items():
            if isinstance(value, str) and value:
                optional_parameters.append(key)
                optional_parameters.append(value)
            elif value:
                optional_parameters.append(key)

        # Full command
        cmd = [
            "prefetch",
            *optional_parameters,
            sra_id,
        ]

        # Remove empty strings (if any) from command list
        cmd = [arg for arg in cmd if arg]
        full_log_file = self.output_dir / log_file if log_file else None

        try:
            # Run prefetch: capture output in log file
            if full_log_file:
                with open(full_log_file, "w") as f:  # Open file for writing
                    subprocess.run(cmd, check=True, stdout=f, stderr=f, text=True)
            # Run prefetch without a log file
            else:
                subprocess.run(cmd, check=True, text=True)

            # Check download
            self._verify_download(full_log_file, srr_list=[sra_id], file_mode="a")
            print(f"Successfully downloaded {sra_id}" + "-" * 30)

        except subprocess.CalledProcessError as e:

            # Log the error but do not raise it
            print(f"Error downloading {sra_id}: Check log file: {full_log_file}")
            if full_log_file:
                error_message = f"Error downloading {sra_id}: {e}"
                with open(full_log_file, "a") as f:
                    f.write(error_message)
            else:
                print(error_message)

            # Try the last resource to download with AWS links
            self._get_sra_aws_links(sra_id)
            return  # Move to the next SRR without stopping execution

    def _get_sra_aws_links(self, sra_id: str, local_mode: bool=False) -> bool:
        """
        Verifies if the SRR is a prefetch version or AWS link version.

        1. Extract AWS download links from NCBI SRA Run Browser using Selenium.
        2. Creates and executes a manual AWS download script for an SRA ID if 
           the files are only available in AWS. Returns True.
        3. Returns False if files available only through prefetch.

        Parameters
        ----------
        sra_id : str
            The SRA ID to verify/download (e.g., "SRR31810743").

        Returns
        -------
        bool
            True if it is an AWS-only SRR or False if prefetch can be performed.
        """

        if local_mode:
            from webdriver_manager.chrome import ChromeDriverManager

        # Define the URL
        url = (
            f"https://trace.ncbi.nlm.nih.gov/Traces/index.html?"
            f"view=run_browser&acc={sra_id}&display=data-access"
        )

        # Selenium options
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Set up Selenium WebDriver (headless mode)
        if local_mode:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        else:
            options.binary_location = CHROME_BIN
            service = Service(CHROMEDRIVER_BIN)
            driver = webdriver.Chrome(service=service, options=options)

        try:
            # Load the page
            driver.get(url)
            time.sleep(5)  # Wait for JavaScript to load the content

            # Get the updated page source with JavaScript-rendered content
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract all AWS download links
            aws_links = [
                a["href"]
                for a in soup.find_all("a", href=True)
                if "https://sra-pub-src" in a["href"]
            ]

            if not aws_links:
                return False

            print(f"SRA = {sra_id} is AWS-only. Downloading via HTTPS instead.")

            # Define the bash script file path
            bash_file_name = self.output_dir / f"prefetch_{sra_id}.sh"
            bash_file_name_log = self.output_dir / f"prefetch_{sra_id}.log"

            # If the script already exists, assume the download was scheduled before
            bash_file_exists = False
            if bash_file_name.exists() or bash_file_name_log.exists():
                print(f"Bash script {bash_file_name} already exists. Skipping creation.")
                print((f"If posterior execution fails, remove ",
                       f"{bash_file_name} and {bash_file_name_log} scripts."))
                bash_file_exists = True

            if not bash_file_exists:

                # Write the bash script
                with open(bash_file_name, "w") as bash_file:
                    bash_file.write("#!/bin/bash\n\n")
                    bash_file.write("# Define URLs and output file names\n")
                    bash_file.write("urls=(\n")
                    for aws_link in aws_links:
                        bash_file.write(f'    "{aws_link}"\n')
                    bash_file.write(")\n\n")
                    bash_file.write("output_files=(\n")
                    for aws_link in aws_links:
                        aws_link_name = os.path.basename(aws_link).removesuffix(".1")
                        output_file = self.output_dir / f"{sra_id}_{aws_link_name}"
                        bash_file.write(f'    "{output_file}"\n')
                    bash_file.write(")\n\n")
                    bash_file.write("# Loop through URLs and download each file\n")
                    bash_file.write('for i in "${!urls[@]}"; do\n')
                    bash_file.write('    echo "Downloading: ${urls[i]} -> ${output_files[i]}"\n')
                    bash_file.write('    wget -O "${output_files[i]}" "${urls[i]}"\n')
                    bash_file.write('    echo "Verifying GZIP Files..."\n')
                    bash_file.write('    if gzip -t "${output_files[i]}" 2>/dev/null; then\n')
                    bash_file.write('        echo "File: ${output_files[i]} is OK"\n')
                    bash_file.write('    else\n')
                    bash_file.write('        echo "File: ${output_files[i]} is CORRUPTED"\n')
                    bash_file.write('    fi\n')
                    bash_file.write("done\n")

                # Make the script executable
                bash_file_name.chmod(0o755)

            # Run the script with nohup in the background
            if not bash_file_name.exists() and not bash_file_name_log.exists():
                nohup_command = f"nohup bash {bash_file_name} > {bash_file_name_log} 2>&1 &"
                subprocess.run(nohup_command, shell=True, check=False)

                print(f"Started AWS download for {sra_id}. Logs: {bash_file_name_log}")

            return True # prefetch does not exist

        except Exception as e:
            print(f"Error fetching AWS links: {e}")
            return False # prefetch exists

        finally:
            driver.quit()  # Close the browser session

    def _verify_download(self, log_file_name: str, srr_list: list=None, file_mode: str="w") -> None:
        """
        Validate downloaded raw sequencing data files using vdb-validate and gzip.

        This method performs validation of files downloaded via `prefetch` (typically `.sralite` or `.sra`)
        and files downloaded manually (typically `.fastq.gz`), writing all log output to the specified
        log file.

        Parameters
        ----------
        log_file_name : str
            Path to the log file where all validation logs will be written.
        srr_list : list of str, optional
            A list of SRR accession identifiers. If provided, only files related to these SRRs
            will be validated. If None, all files in the relevant directories will be validated.

        Notes
        -----
        - Prefetched files are expected to reside in `self.ncbi_dir` with extensions `.sralite` or `.sra`.
        - Non-prefetch files (e.g., `.fastq.gz`) are expected to reside in `self.output_dir`.
        - `vdb-validate` is used for SRA/SRALITE validation.
        - `gzip -t` is used to test gzip integrity for FASTQ files.
        """

        # Get all relevant files
        sra_files = glob.glob(os.path.join(self.ncbi_dir, '*.sralite')) + \
                    glob.glob(os.path.join(self.ncbi_dir, '*.sra'))

        fastq_files = glob.glob(os.path.join(self.output_dir, '*.fastq.gz'))

        # If SRR list is given, filter only the corresponding SRA/SRALITE files
        if srr_list:
            srr_set = set(srr_list)
            sra_files = [f for f in sra_files if os.path.splitext(os.path.basename(f))[0] in srr_set]
            fastq_files = [] # In this case, fastq_files is not performed

        # Open the log file for writing output of all validations
        with open(log_file_name, file_mode) as log_file:

            # First validate SRA/SRALITE files using vdb-validate
            log_file.write("Validating SRA/SRALITE files with vdb-validate:\n")
            for sra_path in sra_files:
                if os.path.exists(sra_path):
                    log_file.write(f"\nRunning vdb-validate on: {sra_path}\n")
                    try:
                        result = subprocess.run(
                            ['vdb-validate', sra_path],
                            capture_output=True,
                            text=True
                        )
                        log_file.write(result.stdout)
                        if result.stderr:
                            log_file.write("\n[stderr]\n" + result.stderr)
                    except Exception as e:
                        log_file.write(f"Error running vdb-validate on {sra_path}: {e}\n")
                else:
                    log_file.write(f"File not found: {sra_path}\n")

            # Then validate fastq.gz files using gzip -t
            log_file.write("\n\nValidating .fastq.gz files with gzip -t:\n")
            for fastq_path in fastq_files:
                if os.path.exists(fastq_path):
                    log_file.write(f"\nRunning gzip -t on: {fastq_path}\n")
                    try:
                        result = subprocess.run(
                            ['gzip', '-t', fastq_path],
                            capture_output=True,
                            text=True
                        )
                        if result.returncode == 0:
                            log_file.write("OK\n")
                        else:
                            log_file.write("FAILED\n")
                            if result.stderr:
                                log_file.write(result.stderr)
                    except Exception as e:
                        log_file.write(f"Error running gzip -t on {fastq_path}: {e}\n")
                else:
                    log_file.write(f"File not found: {fastq_path}\n")

    def _process_sra_to_fastq(self,
                              sra_file : str,
                              output_format : str = "",
                              threads : str = "4",
                              bufsize : str = "8MB",
                              curcache : str = "128MB",
                              mem : str = "24GB",
                              disk_limit : str = "",
                              disk_limit_tmp : str = "",
                              min_read_len : str = "",
                              only_aligned : bool = False,
                              only_unaligned : bool = False,
                              skip_technical : bool = False,
                              include_technical : bool = True,
                              split_files : bool = True,
                              split_3 : bool = True,
                              concatenate_reads : bool = False,
                              split_spot : bool = False,
                              table : str = "",
                              bases : bool = False,
                              internal_ref : bool = False,
                              external_ref : bool = False,
                              ref_name : bool = False,
                              ref_report : bool = False,
                              use_name : bool = False,
                              log_level : str = "5",
                              verbose : bool = True,
                              progress : bool = False,
                              details : bool = False,
                              quiet : bool = False,
                              fasta : bool = False,
                              fasta_unsorted : bool = False,
                              fasta_ref_tbl : bool = False,
                              fasta_concat_all : bool = False,
                              temp_directory : str = "tmp_dir",
                              output_file : str = "",
                              output_directory : str = "out_dir") -> None:
        """
        Process SRA file to retrieve the corresponding fastq file(s).

        This method runs 'fastq-dump' with configurable options on downloaded 
        raw sequencing data from **NCBI SRA** converting it into FASTQ format.

        Usage:
          fasterq-dump <path> [options]
          fasterq-dump <accession> [options]

        Options:
          -F|--format                      format (special, fastq, default=fastq).
          -e|--threads                     how many thread dflt=6.
          -b|--bufsize                     size of file-buffer dflt=1MB.
          -c|--curcache                    size of cursor-cache dflt=10MB.
          -m|--mem                         memory limit for sorting dflt=100MB.
          --disk-limit                     explicitly set disk-limit.
          --disk-limit-tmp                 explicitly set disk-limit for temp files.
          -M|--min-read-len                filter by sequence-len.
          -a|--only-aligned                process only aligned reads.
          -U|--only-unaligned              process only unaligned reads.
          --skip-technical                 skip technical reads.
          --include-technical              include technical reads.
          -S|--split-files                 write reads into different files.
          -3|--split-3                     writes single reads in special file.
          --concatenate-reads              writes whole spots into one file.
          -s|--split-spot                  split spots into reads.
          --table                          which seq-table to use in case of pacbio.
          -B|--bases                       filter by bases.
          --internal-ref                   extract only internal REFERENCEs.
          --external-ref                   extract only external REFERENCEs.
          --ref-name                       extract only these REFERENCEs.
          --ref-report                     enumerate references.
          --use-name                       print name instead of seq-id.
          -L|--log-level <level>           Logging level as number or enum string. One 
                                           of (fatal|sys|int|err|warn|info|debug) or 
                                           (0-6) Current/default is warn.
          -v|--verbose                     Increase the verbosity of the program 
                                           status messages. Use multiple times for more
                                           verbosity. Negates quiet. 
          -p|--progress                    show progress.
          -x|--details                     print details.
          -q|--quiet                       Turn off all status messages for the 
                                           program. Negated by verbose.
          --fasta                          produce FASTA output.
          --fasta-unsorted                 produce FASTA output, unsorted.
          --fasta-ref-tbl                  produce FASTA output from REFERENCE tbl.
          --fasta-concat-all               concatenate all rows and produce FASTA.
          -t|--temp                        where to put temp. files dflt=curr dir.
          -o|--outfile                     output-file.
          -O|--outdir                      output-dir.

        Parameters
        ----------
        sra_file : str
            Path to the SRA file to convert.
        output_format : Placeholder
            Placeholder
        threads : Placeholder
            Placeholder
        bufsize : Placeholder
            Placeholder
        curcache : Placeholder
            Placeholder
        mem : Placeholder
            Placeholder
        disk_limit : Placeholder
            Placeholder
        disk_limit_tmp : Placeholder
            Placeholder
        min_read_len : str, optional
            Minimum read length (default: "").
        only_aligned : Placeholder
            Placeholder
        only_unaligned : Placeholder
            Placeholder
        skip_technical : bool, optional
            Skip technical reads (default: False).
        include_technical : Placeholder
            Placeholder
        split_files : bool, optional
            Split output into separate files per read (default: False).
        split_3 : bool, optional
            Split paired-end reads into forward and reverse files (default: True).
        concatenate_reads : Placeholder
            Placeholder
        split_spot : bool, optional
            Split spot group information (default: False).
        table : Placeholder
            Placeholder
        bases : Placeholder
            Placeholder
        internal_ref : Placeholder
            Placeholder
        external_ref  : Placeholder
            Placeholder
        ref_name : Placeholder
            Placeholder
        ref_report  : Placeholder
            Placeholder
        use_name : Placeholder
            Placeholder
        log_level : str, optional
            Logging level (default: "5").
        verbose : Placeholder
            Placeholder
        progress : Placeholder
            Placeholder
        details : Placeholder
            Placeholder
        quiet : Placeholder
            Placeholder
        fasta : bool, optional
            Output sequences in FASTA format instead of FASTQ (default: False).
        fasta_unsorted  : Placeholder
            Placeholder
        fasta_ref_tbl : Placeholder
            Placeholder
        fasta_concat_all : Placeholder
            Placeholder
        temp_directory : Placeholder
            Placeholder
        output_file : str, optional
            File name where FASTQ files will be saved (default: [fastrq-dump default]).
        output_directory : str, optional
            Directory where FASTQ files will be saved (default: "output_directory").

        Raises
        ------
        ValueError
            If 'sra_id' is empty or not a valid SRA accession.
        FileNotFoundError
            If 'fastq-dump' is not installed or not found in the system path.
        subprocess.CalledProcessError
            If 'fastq-dump' execution fails (e.g., due to network issues or NCBI restrictions).

        Examples
        --------
        >>> geo_sra_downloader._process_sra_to_fastq("./SRR123456.sra")
        Running fastq-dump for SRR123456...
        Finished fastq-dump for SRR123456

        >>> geo_sra_downloader._process_sra_to_fastq("./SRR789012.sra", split_3=True, gzip_files=True)
        Running fastq-dump for SRR789012...
        Finished fastq-dump for SRR789012
        """

        # Check SRA ID
        if not sra_file:
            raise ValueError(f"Invalid SRA file name provided: {sra_file}")

        print(f"Running fasterq-dump for {sra_file}..." + "-"*30)

        # Ensure output directory exists
        if output_directory:
            output_directory = Path(output_directory)
            output_directory.mkdir(parents=True, exist_ok=True)

        # Ensure temp directory exists
        if temp_directory:
            temp_directory = Path(temp_directory)
            temp_directory.mkdir(parents=True, exist_ok=True)

        # Define command-line parameters using a dictionary
        fasterq_dump_params = {
            "--format": output_format,
            "--threads": threads,
            "--bufsize": bufsize,
            "--curcache": curcache,
            "--mem": mem,
            "--disk-limit": disk_limit,
            "--disk-limit-tmp": disk_limit_tmp,
            "--min-read-len": min_read_len,
            "--only-aligned": only_aligned,
            "--only-unaligned": only_unaligned,
            "--skip-technical": skip_technical,
            "--include-technical": include_technical,
            "--split-files": split_files,
            "--split-3": split_3,
            "--concatenate-reads": concatenate_reads,
            "--split-spot": split_spot,
            "--table": table,
            "--bases": bases,
            "--internal-ref": internal_ref,
            "--external-ref": external_ref,
            "--ref-name": ref_name,
            "--ref-report": ref_report,
            "--use-name": use_name,
            "--log-level": log_level,
            "--verbose": verbose,
            "--progress": progress,
            "--details": details,
            "--quiet": quiet,
            "--fasta": fasta,
            "--fasta-unsorted ": fasta_unsorted,
            "--fasta-ref-tbl": fasta_ref_tbl,
            "--fasta-concat-all": fasta_concat_all,
            "--temp": temp_directory,
            "--outfile": output_file,
            "--outdir": output_directory,
        }

        # Convert dictionary into a cleaned list of CLI arguments
        optional_parameters = []
        for key, value in fasterq_dump_params.items():
            if isinstance(value, (str, Path)) and value:
                optional_parameters.append(key)
                optional_parameters.append(str(value))
            elif value:
                optional_parameters.append(key)

        # Full command
        cmd = [
            "fasterq-dump",
            *optional_parameters,
            sra_file,
        ]

        # Remove empty strings (if any) from command list
        cmd = [str(arg) for arg in cmd if arg]
        sra_id = Path(sra_file).stem
        full_log_file = output_directory / f"fasterqdump_{sra_id}.log" if output_directory else None

        # Running fasterq-dump
        print(f"Running command: {' '.join(cmd)}")
        try:
            # Run fasterq-dump and capture errors if any
            if full_log_file:
                with open(full_log_file, "w") as f:  # Open file for writing
                    subprocess.run(cmd, check=True, stdout=f, stderr=f, text=True)
            else:
                subprocess.run(cmd, check=True, text=True)

            print(f"Successfully downloaded {sra_id}" + "-" * 30)

            # Compress files after successful execution
            self._compress_fasterq_outputs(output_directory, sra_id)

        except subprocess.CalledProcessError:
            print(f"Error downloading {sra_id}. Check log file: {full_log_file}")
            # Do not raise, continue to next.
            return

    def _compress_fasterq_outputs(self, output_dir: Path, sra_id: str, dry_run: bool = False):
        """
        Compress all FASTQ files generated by fasterq-dump for a given SRR ID.

        This function searches for files matching the SRR ID prefix in the specified output directory
        and compresses them using gzip, deleting the original uncompressed FASTQ files afterward.

        Parameters
        ----------
        output_dir : Path
            Directory containing the FASTQ files to compress.
        sra_id : str
            The SRR ID used as prefix to identify related FASTQ files.
        dry_run : bool, optional
            If True, only print actions without executing (default is False).
        """

        fastq_files = sorted(output_dir.glob(f"{sra_id}*.fastq"))

        if not fastq_files:
            print(f"[compress_fasterq_outputs] No FASTQ files found for {sra_id} in {output_dir}")
            return

        for fastq_file in fastq_files:
            gz_file = fastq_file.with_suffix(fastq_file.suffix + ".gz")
            print(f"[compress_fasterq_outputs] Compressing: {fastq_file} → {gz_file}")

            if not dry_run:
                with open(fastq_file, "rb") as f_in, gzip.open(gz_file, "wb") as f_out:
                    f_out.writelines(f_in)
                os.remove(fastq_file)
                print(f"[compress_fasterq_outputs] Removed original: {fastq_file}")
            else:
                print(f"[compress_fasterq_outputs] (Dry run) Would compress and remove: {fastq_file}")

    def __repr__(self) -> str:
        """
        Official string representation of the class instance.

        This method returns a detailed representation of the object,
        which is useful for debugging and logging.

        Returns
        -------
        str
            A string containing the class name, GEO ID, and output directory.

        Examples
        --------
        >>> downloader = GEODataDownloader("GSE285812", "data/raw")
        >>> repr(downloader)
        'GEODataDownloader(geo_id="GSE285812", output_dir="data/raw")'
        """
        return f'GEODataDownloader(geo_id="{self.geo_id}", output_dir="{self.output_dir}")'

    def __str__(self) -> str:
        """
        User-friendly string representation of the class instance.

        This method returns a human-readable summary of the instance,
        typically used when printing the object.

        Returns
        -------
        str
            A descriptive string with key details about the downloader instance.

        Examples
        --------
        >>> downloader = GEODataDownloader("GSE285812", "data/raw")
        >>> print(downloader)
        '[GEODataDownloader] GEO ID: GSE285812 | Output Directory: data/raw'
        """
        return f'[GEODataDownloader] GEO ID: {self.geo_id} | Output Directory: {self.output_dir}'

    def cleanup(self):
        if self._gse is not None and self._temp_file_name and self._temp_file_name.exists():
            print(f"Cleaning up temporary files at {self._temp_file_name}")
            shutil.rmtree(self._temp_file_name)

