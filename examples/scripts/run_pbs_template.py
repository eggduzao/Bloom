import os
import sys
from pathlib import Path

# Define the base path of your project
current_path = Path().resolve()
project_root = current_path.parent.parent # Moves 2 levels up from Bloom/bloom/data/ to Bloom

print(project_root)

# Add project root to sys.path
sys.path.append(str(project_root))

# Now you can import the module\n",
from bloom.data.geo_sra_downloader import GEODataDownloader

class RunPBS:

    def __init__(self, geo_id, num_workers, download_path):

        self.geo_id = geo_id
        self.num_workers = num_workers
        self.download_path = download_path
        self.geo_downloader = GEODataDownloader(self.geo_id, self.download_path)

    def create_metadata(self):

        self.geo_downloader.create_metadata_table()

    def download(self):

        self.geo_downloader.download_raw_data(self.num_workers)

    def create_files(self):

        # Create PBS scripts
        for i, param in enumerate(["Place", "holder"]):

            # Parameters
            input_location = os.path.join(self.download_path, param)
            output_location = os.path.join(self.download_path, param)

            # Unique PBS file name
            pbs_filename = f"{self.geo_id}_{i}.pbs"

            # Create PBS script
            with open(pbs_filename, "w") as pbs_file:
                pbs_file.write(
                    f"""#!/bin/bash

#PBS -N {self.geo_id}_{i}
#PBS -o {self.geo_id}_{i}.out
#PBS -e {self.geo_id}_{i}.err

#PBS -q workq
# workq - Fila default e sem restrições. Utiliza todos os nós.
# fatq - fila para os fat nodes.
# normq - fila para nodes comuns.
# gpuq - fila para processamento em GPU.
#PBS -V
#PBS -W umask=002

#PBS -l nodes=1:ppn=4
#PBS -l mem=48gb
#PBS -l walltime=12:00:00

# cd $PBS_O_WORKDIR

# Environments
source /sw/miniconda3/bin/activate
conda activate ml

# Current Job Parameter
basepath=\"{self.geo_id}\"

# Create output path and move to input location
mkdir -p \"$output_location\"
cd $basepath

# Uncompress Control
# Code goes here.

"""
                )

    def run_jobs(self):

        # Submit PBS scripts
        for i, param in enumerate(["Place", "holder"]):

            # Unique PBS file name
            pbs_filename = f"{self.geo_id}_{i}.pbs"

            # Submit job
            os.system(f"qsub {pbs_filename}")

    def merge_files(self):

        # Get name of files
        out_file_list = []
        err_file_list = []
        for i, param in enumerate(["Place", "holder"]):

            # Unique out and err PBS file name
            out_filename = f"{self.geo_id}_{i}.out"
            err_filename = f"{self.geo_id}_{i}.err"

            # Append to list only if it exists
            if os.path.exists(out_filename):
                out_file_list.append(out_filename)
            if os.path.exists(err_filename):
                err_file_list.append(err_filename)

        # Output file name
        out_file_merged = f"{self.geo_id}_merged.out"
        err_file_merged = f"{self.geo_id}_merged.err"

        # Merge only if list is not empty
        if len(out_file_list) >= 1:
            self._merge(out_file_list, out_file_merged)
        if len(err_file_list) >= 1:
            self._merge(err_file_list, err_file_merged)

    def delete_files(self):

        # Submit PBS scripts
        for i, param in enumerate(["Place", "holder"]):

            # Unique PBS, out and err file name
            pbs_filename = f"{self.geo_id}_{i}.pbs"
            out_filename = f"{self.geo_id}_{i}.out"
            err_filename = f"{self.geo_id}_{i}.err"

            # Removing files
            if os.path.exists(pbs_filename):
                os.remove(pbs_filename)
            if os.path.exists(out_filename):
                os.remove(out_filename)
            if os.path.exists(err_filename):
                os.remove(err_filename)

    def _merge(self, file_list, output_file):
        # Merge files
        with open(output_file, "w") as outfile:
            for file in file_list:
                outfile.write(f"> {file}\n")  # Write the filename as a header
                with open(file, "r") as infile:
                    outfile.write(infile.read())  # Append file content
                outfile.write(
                    ("-" * 50) + "\n\n"
                )  # Add 50 dashes and 2 blank lines at the end

if __name__ == "__main__":

    # Parameters
    geo_id = "GSE285812"
    num_workers = 3
    operation = sys.argv[1]

    # Dataset
    base_path = "/storage2/egusmao/projects/Bloom/data/"
    # base_path = "/Users/egg/Projects/Bloom/data/"
    download_path = os.path.join(base_path, "raw")

    # Input handling
    run_pbs = RunPBS(geo_id, num_workers, download_path)

    # Operation
    if operation == "make":
        run_pbs.create_metadata()
    elif operation == "run":
        run_pbs.download()
