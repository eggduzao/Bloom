from __future__ import print_function
"""
Pipeline Test
===================
Placeholder.

Authors: Eduardo G. Gusmao.

"""

###################################################################################################
# Libraries
###################################################################################################

# Python
import os
import sys
import subprocess

# Internal
from bloom.preprocess import Preprocess
from bloom.sica import Sica
from bloom.goba import Goba
from bloom.dpmm import Dpmm
from bloom.ifs import Ifs

# External
import numpy as np


###################################################################################################
# PipelineTest Class
###################################################################################################

class PipelineTest():
  """Placeholder.

  *Keyword arguments:*

    - argument1 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.

    - argument2 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.
  """

  def __init__(self, input_location, temporary_location, output_location):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Class objects
    self.input_location = input_location
    self.temporary_location = temporary_location
    self.output_location = output_location

    # Creating folders
    for folder_name in [self.input_location, self.temporary_location, self.output_location]:
      if(not os.path.exists(folder_name)):
        folder_creation_command = ["mkdir", "-p", folder_name]
        folder_creation_process = subprocess.run(folder_creation_command , stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

  def write_list(self, name, list_to_write, output_file):
    """Write list_to_write to output_file
    """
    output_file.write("### " + name + "\n")
    if(list_to_write):
      for i in range(0, len(list_to_write)):
        output_file.write(str(i) + ": " + str(list_to_write[i]) + "\n")
    else:
      output_file.write("None\n")
    output_file.write("\n")

  def write_dict(self, name, dict_to_write, output_file):
    """Write dict_to_write to output_file
    """
    output_file.write("### " + name + "\n")
    if(dict_to_write):
      keys = sorted(dict_to_write.keys())
      if(keys):
        for k in keys:
          output_file.write(str(k) + ": " + str(dict_to_write[k]) + "\n")
      else:
        output_file.write("None\n")
    else:
      output_file.write("None\n")
    output_file.write("\n")

  def write_contact_map(self, name, contact_map, output_file):
    """Write contact_map matrix to output_file
    """
    output_file.write("### " + name + "\n")
    if(contact_map and contact_map.matrix):
      keys = sorted(contact_map.matrix.keys())
      if(keys):
        for k in keys:
          regions = sorted(contact_map.matrix[k].keys(), key = lambda x: x[0])
          if(regions):
            for r in regions:
              output_file.write("\t".join([str(k), str(r[0]), str(r[1]), str(contact_map.matrix[k][r])]) + "\n")
          else:
            output_file.write(str(k) + ": " + "None\n")
      else:
        output_file.write("None\n")
    else:
      output_file.write("None\n")
    output_file.write("\n")

  def write_matrix(self, name, matrix, output_file):
    """Write dict_to_write to output_file
    """
    output_file.write("### " + name + "\n")
    if(matrix.size != 0):
      counter = 0
      for vec in matrix:
        output_file.write("[" + str(counter) + "]\t".join([str(e) for e in vec]) + "\n")
        counter += 1
    else:
      output_file.write("None\n")
    output_file.write("\n")



  ###################################################################################################
  # 8. Preprocess
  ###################################################################################################

  def convert_to_minimal_resolution(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Output file
    output_file_name = os.path.join(self.output_location, "convert_to_minimal_resolution.txt")
    output_file = open(output_file_name, "w")

    # TODO

    # Termination
    output_file.close()


  def convert_to_minimal_resolution(self, recalculate_statistics = True):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Create new contact map
    new_contact_map = ContactMap(organism = self.input_contact_map.organism, resolution = self.minimal_resolution, matrix = None)

    # Iterating on valid chromosomes
    for chromosome in new_contact_map.valid_chromosome_list:

      # Add reshape process to list
      self.add_reshape(chromosome, new_contact_map)

    # Execute reshape
    self.run_reshape()

    # Recalculate statistics
    if(recalculate_statistics):
      new_contact_map.update_valid_chromosome_list()
      new_contact_map.calculate_all_statistics()

    # Return new contact map
    return new_contact_map






  def main_remove_blacklist(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Output file
    output_file_name = os.path.join(self.output_location, "main_remove_blacklist.txt")
    output_file = open(output_file_name, "w")

    # TODO

    # Termination
    output_file.close()


  def main_remove_blacklist(self, contact_map):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Get valid chromosome list
    valid_chromosome_list = contact_map.valid_chromosome_list

    # Iterating on valid chromosomes
    for chromosome in valid_chromosome_list:

      # Add chromosome to dictionaries
      try:
        self.removed_dict[chromosome]
      except Exception:
        self.removed_dict[chromosome] = dict()

      # Add remove_from_map job to the queue
      self.add_remove_blacklist(chromosome, contact_map)

    # Run remove_from_map
    self.run_remove_blacklist()







  def main_void_statistics(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Output file
    output_file_name = os.path.join(self.output_location, "main_void_statistics.txt")
    output_file = open(output_file_name, "w")

    # TODO

    # Termination
    output_file.close()


  def main_void_statistics(self, contact_map):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """




  ###################################################################################################
  # 9. SICA
  ###################################################################################################



  def main_calculate_distributions(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Output file
    output_file_name = os.path.join(self.output_location, "main_calculate_distributions.txt")
    output_file = open(output_file_name, "w")

    # TODO

    # Termination
    output_file.close()


  def main_calculate_distributions(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Iterating on valid chromosomes - Calculate histograms
    for chromosome in self.contact_map.valid_chromosome_list:

      # Put chromosome in distribution_dictionary, annotation dictionary and dist_to_diag_dictionary
      self.distribution_dictionary[chromosome] = dict()
      self.annotation_dictionary[chromosome] = dict()
      self.dist_to_diag_dictionary[chromosome] = dict()

      # Add histogram calculation job to queue
      self.add_calculate_histogram(chromosome)

    # Run histogram calculation jobs
    self.run_calculate_histogram()

    # Iterating on valid chromosomes - Calculate pvalues
    for chromosome in self.contact_map.valid_chromosome_list:

      # Put chromosome in pvalue_dictionary
      self.pvalue_dictionary[chromosome] = dict()

      # Iterating on SicaDist
      for skey, svalue in self.dist_handler.sica_dist_dict.items():

        # Add p-value calculation job to queue
        self.add_calculate_pvalues(chromosome, svalue)

    # Run p-value calculation jobs
    self.run_calculate_pvalues()







  def main_star_contacts(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Output file
    output_file_name = os.path.join(self.output_location, "main_star_contacts.txt")
    output_file = open(output_file_name, "w")

    # TODO

    # Termination
    output_file.close()


  def main_star_contacts(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Iterating on valid chromosomes - Starring contacts
    for chromosome in self.contact_map.valid_chromosome_list:

      # Add histogram calculation job to queue
      self.add_star_contacts(chromosome)

    # Run histogram calculation jobs
    self.run_star_contacts()








  ###################################################################################################
  # 10. GOBA
  ###################################################################################################

  def main_fill(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Output file
    output_file_name = os.path.join(self.output_location, "main_fill.txt")
    output_file = open(output_file_name, "w")

    # TODO

    # Termination
    output_file.close()


  def main_fill(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Iterating on valid chromosomes - Calculate histograms
    for chromosome in self.contact_map.valid_chromosome_list:

      # Add histogram calculation job to queue
      self.add_fill(chromosome)

    # Run histogram calculation jobs
    self.run_fill()








  ###################################################################################################
  # 11. DPMM
  ###################################################################################################



  def diagonal_degrade(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Output file
    output_file_name = os.path.join(self.output_location, "diagonal_degrade.txt")
    output_file = open(output_file_name, "w")

    # TODO

    # Termination
    output_file.close()


  def diagonal_degrade(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Get valid chromosome list
    valid_chromosome_list = self.contact_map.valid_chromosome_list
    
    # Iterating on valid chromosomes
    for chromosome in valid_chromosome_list:

      # Add introduce_squares to the queue
      self.add_degrade(self.contact_map, chromosome)

    # Run introduce squares
    self.run_degrade()








  def introduce_shapes(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Output file
    output_file_name = os.path.join(self.output_location, "introduce_shapes.txt")
    output_file = open(output_file_name, "w")

    # TODO

    # Termination
    output_file.close()

  def introduce_shapes(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """





  ###################################################################################################
  # 12. IFS
  ###################################################################################################


  def main_calculate_ifs(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Output file
    output_file_name = os.path.join(self.output_location, "main_calculate_ifs.txt")
    output_file = open(output_file_name, "w")

    # TODO

    # Termination
    output_file.close()


  def main_calculate_ifs(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Iterating on valid chromosomes - Calculate histograms
    for chromosome in self.contact_map.valid_chromosome_list:

      # Add histogram calculation job to queue
      self.add_calculate_ifs(chromosome)

    # Run histogram calculation jobs
    self.run_calculate_ifs()

    # Sort and write IFS list
    self.sort_ifs_list()
    self.standardize_ifs_list(min_to_zero = True)
    self.write_ifs()






  def main_fix_matrix(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Output file
    output_file_name = os.path.join(self.output_location, "main_fix_matrix.txt")
    output_file = open(output_file_name, "w")

    # TODO

    # Termination
    output_file.close()

  def main_fix_matrix(self, multiplier = 1000, min_matrix_threshold = 1):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Iterating on valid chromosomes - Calculate histograms
    for chromosome in self.contact_map.valid_chromosome_list:

      # Add histogram calculation job to queue
      self.add_fix_matrix(chromosome, multiplier, min_matrix_threshold)

    # Run histogram calculation jobs
    self.run_fix_matrix()

    # Write matrix
    self.write_matrix()






###################################################################################################
# Execution
###################################################################################################

if __name__ == "__main__":

  # Fixed Parameters
  current_name = os.path.splitext(os.path.basename(__file__))[0]
  current_path = os.path.dirname(os.path.abspath(__file__))
  input_location = os.path.join(current_path, "input")
  temporary_location = os.path.join(current_path, "temp", current_name)
  output_location = os.path.join(current_path, "output", current_name)
  
  # Creating test
  test = PipelineTest(input_location, temporary_location, output_location)

  # Tests
  test.xxxxx()
