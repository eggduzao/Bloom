"""
IO Juicer Module
===================
Placeholder.

Authors: Eduardo G. Gusmao.

"""

###################################################################################################
# Libraries
###################################################################################################

# Python
import os
import gc
import sys
import codecs
import traceback
import subprocess
import configparser
import multiprocessing

# Internal
from bloom.util import ConfigurationFile, ChromosomeSizes, ErrorHandler

# External


###################################################################################################
# Juicer Auxiliary Class
###################################################################################################

class Juicer(ConfigurationFile):
  """This class represents TODO.

  *Keyword arguments:*

    - argument1 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.

    - argument2 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.
  """

  def __init__(self, ncpu):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Configuration file initialization
    ConfigurationFile.__init__(self)
    self.juicer_command = self.config.get("Juicer", "command")
    self.juicer_options = self.config.get("Juicer", "options")
    self.juicer_jar_location = os.path.join(self.bloom_data_path, self.config.get("Juicer", "jar"))

    # Auxiliary parameters
    self.ncpu = ncpu
    self.process_queue = []
    self.kind_of_matrix = "observed"
    self.kind_of_normalization = "NONE"
    self.unit_of_resolution = "BP"
    self.juicer_resolution_list = [str(i*1000) for i in [1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500]]

    # Error handler
    self.error_handler = ErrorHandler()

  def dump(self, resolution, region1, region2, input_file_name, output_file_name):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
  
    # Execution of Juicer's dump
    command = [self.juicer_command] + self.juicer_options.split(" ") + [self.juicer_jar_location, "dump", 
               self.kind_of_matrix, self.kind_of_normalization, input_file_name,
               region1, region2, self.unit_of_resolution, resolution, output_file_name]
    dump_process = subprocess.run(command , stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    return dump_process

  def add_dump(self, resolution, region1, region2, input_file_name, output_file_name):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    self.process_queue.append((resolution, region1, region2, input_file_name, output_file_name))

  def run_dump(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    
    pool = multiprocessing.Pool(self.ncpu)
    dump_process_output = pool.starmap(self.dump, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()
    pool = None
    self.process_queue = None
    gc.collect()
    successful_execution = True
    for cp in dump_process_output:
      try:
        cp.check_returncode()
      except subprocess.CalledProcessError:
        successful_execution = False # TODO - Error: One or more processes didnt execute correctly.

    return successful_execution

  def sort_pre_file(self, pre_file_name, temporary_location, pre_file_name_sorted):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # 1 - For the first read end chromosome to be less than the second read end chromosome
    temp_sorted_file_name = temporary_location + "temp_sorted_file_name.pre"
    pre_sort_1_command = ["awk", "'{if", "($3", ">", "$7){", "print", "$5,", "$6,", "$7,", "$8,", "$1,", "$2,", "$3,", "$4,", "$9}else", "{print}}'",
                          pre_file_name, ">", temp_sorted_file_name]
    pre_sort_1_process = subprocess.run(pre_sort_1_command , stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

    # 2 - For the reads to be sorted by chromosome block. That is, all chr3R-chr3R reads together in one place. This is so we don’t have to read the file multiple times.
    pre_sort_2_command = ["sort", "-k2,2d", "-k6,6d", temp_sorted_file_name, ">", pre_file_name_sorted]
    pre_sort_2_process = subprocess.run(pre_sort_2_command , stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

    # 3 - Remove the temporary pre file
    pre_sort_3_command = ["rm", "-rf", temp_sorted_file_name]
    pre_sort_3_process = subprocess.run(pre_sort_3_command , stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

  def sparse_matrix_to_pre(self, sparse_matrix_dictionary, pre_file_name):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Opening pre_file_name
    pre_file = open(pre_file_name, "w")

    # Writing matrix to pre_file_name
    for key in sparse_matrix_dictionary.keys():
      kk = key.split(":")
      str1 = "0"; str2 = "1"
      frag1 = "0"; frag2 = "1"
      chr1 = kk[0]; chr2 = kk[0]
      if(chr1 != chr2): continue
      pos1 = kk[1]; pos2 = kk[2]
      score = str(sparse_matrix_dictionary[key])
      vector = [str1, chr1, pos1, frag1, str2, chr2, pos2, frag2, score]
      pre_file.write(" ".join(vector)+"\n")

    # Termination
    pre_file.close()

  def load(self, genome_id, resolution, sparse_matrix_dictionary, temporary_location, output_file_name):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
  
    # Converting sparse matrix to pre file
    pre_file_name = temporary_location + "pre_file_name.pre"
    self.sparse_matrix_to_pre(sparse_matrix_dictionary, pre_file_name)

    # Sorting pre file
    sorted_pre_file_name = temporary_location + "sorted_pre_file_name.pre"
    self.sort_pre_file(pre_file_name, temporary_location, sorted_pre_file_name)

    # Execution of Juicer's pre
    pre_command = [self.juicer_command] + self.juicer_options.split(" ") + [self.juicer_jar_location, "pre", 
                   "-d", "-n", "-r", resolution, "-t", temporary_location, pre_file_name, output_file_name, genome_id]
    pre_process = subprocess.run(pre_command , stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

    # Remove temporary files
    pre_temp_remove_command = ["rm", "-rf", pre_file_name, sorted_pre_file_name]
    pre_temp_remove_process = subprocess.run(pre_temp_remove_command , stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

    return pre_process

  def add_load(self, genome_id, resolution, sparse_matrix_dictionary, temporary_location, output_file_name):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    self.process_queue.append((genome_id, resolution, sparse_matrix_dictionary, temporary_location, output_file_name))

  def run_load(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    
    pool = multiprocessing.Pool(self.ncpu)
    load_process_output = pool.starmap(self.load, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()
    pool = None
    self.process_queue = None
    gc.collect()
    successful_execution = True
    for cp in load_process_output:
      try:
        cp.check_returncode()
      except subprocess.CalledProcessError:
        successful_execution = False # TODO - Error: One or more processes didnt execute correctly.

    return successful_execution

  def identify_minimal_resolution(self, input_file_name, temporary_location, region = "1:1000000:5000000"):

    # Current result resolution
    resolution = None

    # Use built-in functions over the possible resolution list
    for res in self.juicer_resolution_list:

      # Add job
      output_file_name = os.path.join(temporary_location, "res_test_" + res + ".txt")
      self.add_dump(res, region, region, input_file_name, output_file_name)

      # Run job
      successful_execution = self.run_dump()

      # Remove temporary files
      remove_command = ["rm", "-rf", output_file_name]
      remove_process = subprocess.run(remove_command , stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

      # Check resolution
      if(successful_execution):
        resolution = res
        break

    # Return
    return resolution

  def filetype_is_juicer(self, input_file_name, temporary_location, region = "1:1000000:5000000"):

    # Current result resolution
    is_juicer = False

    # Use built-in functions over the possible resolution list
    for res in self.juicer_resolution_list:

      # Add job
      output_file_name = os.path.join(temporary_location, "file_test_" + res + ".txt")
      self.add_dump(res, region, region, input_file_name, output_file_name)

      # Run job
      successful_execution = self.run_dump()

      # Remove temporary files
      remove_command = ["rm", "-rf", output_file_name]
      remove_process = subprocess.run(remove_command , stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

      # Check resolution
      if(successful_execution):
        is_juicer = True
        break

    # Return
    return is_juicer    
