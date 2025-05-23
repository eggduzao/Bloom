from __future__ import print_function
"""
Barcode Module
===================
Placeholder.

Authors: Eduardo G. Gusmao.

"""

# Dictionary in off/barcode_translation.txt

###################################################################################################
# Libraries
###################################################################################################

# Python
import os
import lzma
import random
import codecs
import subprocess

# Internal
from bloom.util import AuxiliaryFunctions
from bloom.io import InputFileType, IO

# External

###################################################################################################
# Barcode Class
###################################################################################################

class Barcode():
  """This class represents TODO.

  *Keyword arguments:*

    - argument1 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.

    - argument2 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.
  """

  def __init__(self, ncpu, organism, contact_map, temporary_location, error_handler, barcode_files, juicer_command, cooler_command, seed = None):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Seed
    if(seed):
      random.seed(seed)

    # Initialization
    self.ncpu = ncpu
    self.organism = organism
    self.contact_map = contact_map
    self.temporary_location = temporary_location
    self.seed = seed

    # Utilitary objects
    self.error_handler = error_handler
    self.barcode_handler = barcode_files
    self.juicer_command = juicer_command
    self.cooler_command = cooler_command


  #############################################################################
  # Main
  #############################################################################

  def main_guide(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Returning files
    final_contact_map = None
    final_loop_list = None

    # Iterate over barcoded cells
    flag_found = False
    for barcode_number in self.barcode_handler.barcode_number_list:

      # Iterate over barcode resolutions
      for barcode_resolution in self.barcode_handler.barcode_res_list:

        # Check resolution
        if(self.contact_map.resolution == barcode_resolution):
          
          # Resolution found
          barcode_list = self.barcode_handler.barcode_file_dictionary[barcode_number]
          compbin_matrix_file_name = barcode_list[0] # barcode_list[2][barcode_resolution] # Use this when testing
          compbin_loop_file_name = barcode_list[1]
          compbin_barcode_file_name = barcode_list[2][barcode_resolution]
          flag_found = True
          break

      # Check if found
      if(flag_found):

        # Decompress barcode
        try:
          barcode_contact_map = self.create_contact_map_from_binary_barcode(compbin_barcode_file_name, resolution = self.contact_map.resolution)
        except Exception:
          continue
          #TODO - Error

        # Compare barcode and current input contact map
        try:
          match = self.match_barcode(barcode_contact_map)
        except Exception:
          continue
          #TODO - Error

        # Check match
        if(match):

          # Decompress matrix and loop
          final_contact_map = self.create_contact_map_from_binary_file(compbin_matrix_file_name, resolution = self.contact_map.resolution)
          final_contact_map.update_valid_chromosome_list()
          final_loop_list = self.create_loop_list_from_binary_file(compbin_loop_file_name, resolution = self.contact_map.resolution)

          # Return objects
          break

        # Return objects
        else:
          continue

    # Return objects
    return final_contact_map, final_loop_list

  def open_lzma_file(self, f, *args, **kwargs):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    try:
      import lzma
    except ImportError:
      raise NotImplementedError('''This version of python doesn't have "lzma" module''')
    if hasattr(lzma, 'open'):
      return lzma.open(f, *args, **kwargs)
    if not isinstance(f, basestring):
      if hasattr(f, 'name') and os.path.exists(f.name):
        f = f.name
      else:
        raise TypeError('Expected `str`, `bytes`, `unicode` or file-like object with valid `name` attribute pointing to a valid path')
    return lzma.LZMAFile(f, *args, **kwargs)

  def string_to_bytelist(self, string):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    if(isinstance(string, str)):
      return [format(ord(i), 'b') for i in string]
    else: 
      raise ValueError("Error: Input must be a string type")

  def bytelist_to_stringlist(self, bytelist):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    if isinstance(bytelist, list):
      return [chr(int(i, 2)) for i in bytelist if i]
    else: 
      raise ValueError("Error: Input must be a list")


  #############################################################################
  # Decompression: Binary -> to -> File
  #############################################################################

  def compbin_to_bg_matrix(self, input_file_name, output_file_name, resolution = 1000):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Input file
    input_file = self.open_lzma_file(input_file_name, mode="rb")
    temporary_file_name = os.path.join(self.temporary_location, "temporary_file_name.bin.txt")
    temporary_file = open(temporary_file_name, "w")

    # Write binary to temporary file
    bytestring = input_file.readline()
    bytelist = self.bytelist_to_stringlist(bytestring.decode("utf8").split(" "))
    temporary_file.write("".join(bytelist))
    temporary_file.close()
    input_file.close()

    # Read and write into the output file
    temporary_file = open(temporary_file_name, "rU")
    output_file = open(output_file_name, "w")
    for line in temporary_file:

      ll = line.strip().split("\t")
      chrom = "chr" + ll[0]
      p11 = AuxiliaryFunctions.expand_integer(ll[1])
      p12 = str(int(p11) + resolution)
      p21 = AuxiliaryFunctions.expand_integer(ll[2])
      p22 = str(int(p21) + resolution)
      v = ll[3]

      out_vec = [chrom, p11, p12, chrom, p21, p22, v]
      output_file.write("\t".join(out_vec) + "\n")

    # Termination
    temporary_file.close()
    output_file.close()

  def compbin_to_bg_loop(self, input_file_name, output_file_name, resolution = 1000):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Input file
    input_file = self.open_lzma_file(input_file_name, mode="rb")
    temporary_file_name = os.path.join(self.temporary_location, "temporary_file_name.bin.txt")
    temporary_file = open(temporary_file_name, "w")

    # Write binary to temporary file
    bytestring = input_file.readline()
    bytelist = self.bytelist_to_stringlist(bytestring.decode("utf8").split(" "))
    temporary_file.write("".join(bytelist))
    temporary_file.close()
    input_file.close()

    # Read and write into the output file
    temporary_file = open(temporary_file_name, "rU")
    output_file = open(output_file_name, "w")
    for line in temporary_file:

      ll = line.strip().split("\t")
      chrom = ll[0]
      p11 = AuxiliaryFunctions.expand_integer(ll[1])
      p12 = AuxiliaryFunctions.expand_integer(ll[2])
      p21 = AuxiliaryFunctions.expand_integer(ll[4])
      p22 = AuxiliaryFunctions.expand_integer(ll[5])
      v = ll[6]

      out_vec = [chrom, p11, p12, chrom, p21, p22, v]
      output_file.write("\t".join(out_vec) + "\n")

    # Termination
    temporary_file.close()
    output_file.close()

  # Convert BINARY FILE -> CONTACT MAP
  def create_contact_map_from_binary_file(self, compbin_matrix_file_name, resolution = 1000):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Convert compbin to regular bedgraph
    matrix_file_name = os.path.join(self.temporary_location, "matrix_file_name")
    self.compbin_to_bg_matrix(compbin_matrix_file_name, matrix_file_name, resolution = resolution)
    
    # Create contact map
    io_instance = IO(matrix_file_name, self.temporary_location, self.organism, self.ncpu, self.error_handler, self.chromosome_sizes, self.juicer_command,
                     self.cooler_command, input_resolution = resolution, input_file_type = InputFileType.SPARSE, seed = self.seed)
    contact_map = io_instance.read()
    contact_map.update_valid_chromosome_list()

    # Return objects
    return contact_map

  # Convert BINARY BARCODE -> CONTACT MAP
  def create_contact_map_from_binary_barcode(self, compbin_barcode_file_name, resolution = 1000):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Convert compbin to regular bedgraph
    barcode_file_name = os.path.join(self.temporary_location, "barcode_file_name")
    self.compbin_to_bg_matrix(compbin_barcode_file_name, barcode_file_name, resolution = resolution)
    
    # Create contact map
    io_instance = IO(barcode_file_name, self.temporary_location, self.organism, self.ncpu, 
                     input_resolution = resolution, input_file_type = InputFileType.SPARSE, seed = self.seed)
    contact_map = io_instance.read()
    contact_map.update_valid_chromosome_list()

    # Return objects
    return contact_map

  # Convert BINARY BARCODE -> CONTACTS (IFS)
  def create_loop_list_from_binary_file(self, compbin_loop_file_name, resolution = 1000):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Convert compbin to regular bedgraph
    loop_file_name = os.path.join(self.temporary_location, "loop_file_name")
    self.compbin_to_bg_loop(compbin_loop_file_name, loop_file_name, resolution = resolution)
    
    # Create contact map
    loop_list = []
    loop_file = open(loop_file_name, "rU")
    for line in loop_file:
      ll = line.strip().split("\t")
      loop_list.append(ll)
    loop_file.close()

    # Return objects
    return loop_list


  #############################################################################
  # Compression: File -> to -> Binary
  #############################################################################

  def bg_to_compbin(self, input_file_name, output_file_name):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    input_file = open(inputFileName, "rU")
    output_file = self.open_lzma_file(input_file_name, mode="wb")

    for line in input_file:

      ll = line.strip().split("\t")
      chrN = ll[0].split("chr")[-1]
      n1 = AuxiliaryFunctions.shorten_integer(ll[1])
      n2 = AuxiliaryFunctions.shorten_integer(ll[2])
      out_string = "\t".join([chrN, n1, n2, ll[3], "\n"])

      bytelist = " ".join(self.string_to_bytelist(out_string)) + " "
      binbytelist = bytearray(bytelist, "utf8")

      output_file.write(binbytelist)

    input_file.close()
    output_file.close()

  def create_binary_file_from_contact_map(self): # TODO
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Convert CONTACT MAP -> BINARY FILE
    # Future - TODO
    pass

  def create_binary_barcode_from_contact_map(self): # TODO
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Convert CONTACT MAP -> BINARY BARCODE
    # Future - TODO
    pass

  def create_binary_contacts_from_loop_list(self): # TODO
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Convert CONTACTS (IFS) -> BINARY BARCODE
    # Future - TODO
    pass


  #############################################################################
  # Check barcode
  #############################################################################

  def match_barcode(self, barcode_contact_map, similarity_degree = 0.01):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Similar object
    is_similar = True
    at_least_one_chromosome = False

    # Iterating on valid chromosomes
    for chromosome in self.contact_map.valid_chromosome_list:

      # Checking existence of matrices
      try:
        self.contact_map.matrix[chromosome]
        at_least_one_chromosome = True
        try:
          barcode_contact_map.matrix[chromosome]
        except Exception:
          is_similar = False
          break
      except Exception:
        continue

      # Match input contact map and barcode
      is_similar = self.contact_map.match_subset(chromosome, barcode_contact_map, similarity_degree = similarity_degree)
      if(is_similar == False):
        break

    # Return objects
    if(at_least_one_chromosome):
      return is_similar
    else: return False


