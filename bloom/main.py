from __future__ import print_function
"""
Main Module
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
import time

# Internal
from bloom.util import ErrorHandler, JuicerCommand, CoolerCommand, ChromosomeSizes, BarcodeFiles, ExcList, Channel, AuxiliaryFunctions
from bloom.arguments import ArgumentParser
from bloom.io import InputFileType, IO
from bloom.contact_map import ContactMap
from bloom.preprocess import Preprocess
from bloom.sica import Sica
from bloom.goba import Goba
from bloom.dpmm import Dpmm
from bloom.ifs import Ifs
from bloom.barcode import Barcode

# External


###################################################################################################
# Tool Execution
###################################################################################################

def main():
  """Entry point to the execution of Bloom.
    
  *Keyword arguments:*
    
    - None.
    
  *Return:*
    
    - None.
  """

  ###############################################################################
  # Error and Warning Handler
  ###############################################################################

  # Initializing ErrorHandler
  error_handler = ErrorHandler()


  ###############################################################################
  # Parameter Handling
  ###############################################################################

  # Initializing argument parser
  argument_parser = ArgumentParser(error_handler)
  args = argument_parser.arguments
  opts = argument_parser.options

  # Arguments
  input_matrix = os.path.abspath(os.path.expanduser(args[0]))
  output_matrix = os.path.abspath(os.path.expanduser(args[1]))
  output_contacts = os.path.abspath(os.path.expanduser(args[2]))

  # Options
  chromosome = opts.chromosome
  organism = opts.organism
  region = opts.region
  resolution = opts.resolution
  input_type = opts.input_type
  cores = opts.cores
  temporary_location = os.path.abspath(os.path.expanduser(opts.temporary_location))
  output_type = opts.output_type
  output_resolution = opts.output_resolution
  avoid_distance = opts.avoid_distance
  fitting_method = opts.fitting_method
  seed = opts.seed

  if(avoid_distance < 0):
    avoid_distance = 5 * output_resolution

  # Hidden Options
  pre_min_contig_removed_bins = opts.pre_min_contig_removed_bins
  pre_remove_threshold = opts.pre_remove_threshold
  sica_pvalue_threshold = opts.sica_pvalue_threshold
  sica_bottom_bin_ext_range = [int(e) for e in opts.sica_bottom_bin_ext_range.split(",")]
  sica_left_bin_ext_range = [int(e) for e in opts.sica_left_bin_ext_range.split(",")]
  sica_right_bin_ext_range = [int(e) for e in opts.sica_right_bin_ext_range.split(",")]
  sica_top_bin_ext_range = [int(e) for e in opts.sica_top_bin_ext_range.split(",")]
  sica_bonuscrosslb_range = [float(e) for e in opts.sica_bonuscrosslb_range.split(",")]
  sica_bonuscross_range = [float(e) for e in opts.sica_bonuscross_range.split(",")]
  sica_bonuslb_range = [float(e) for e in opts.sica_bonuslb_range.split(",")]
  goba_vertical_multiplier = [float(e) for e in opts.goba_vertical_multiplier.split(",")]
  goba_ortogonal_multiplier = [float(e) for e in opts.goba_ortogonal_multiplier.split(",")]
  goba_filling_frequency = opts.goba_filling_frequency
  goba_banding_value_mult_range = [float(e) for e in opts.goba_banding_value_mult_range.split(",")]
  goba_banding_further_range = [float(e) for e in opts.goba_banding_further_range.split(",")]
  goba_banding_frequency = opts.goba_banding_frequency
  goba_outing_value_mult_range = [float(e) for e in opts.goba_outing_value_mult_range.split(",")]
  goba_outing_further_range = [float(e) for e in opts.goba_outing_further_range.split(",")]
  goba_outing_frequency = opts.goba_outing_frequency
  goba_eppoch_resolution = opts.goba_eppoch_resolution
  goba_eppoch_threshold = opts.goba_eppoch_threshold 
  dpmm_random_degrade_range = [float(e) for e in opts.dpmm_random_degrade_range.split(",")]
  dpmm_degrade_multiplier = opts.dpmm_degrade_multiplier
  dpmm_half_length_bin_interval = [int(e) for e in opts.dpmm_half_length_bin_interval.split(",")]
  dpmm_value_range = [float(e) for e in opts.dpmm_value_range.split(",")]
  dpmm_random_range = [float(e) for e in opts.dpmm_random_range.split(",")]
  dpmm_iteration_multiplier = opts.dpmm_iteration_multiplier
  dpmm_em_significant_threshold = opts.dpmm_em_significant_threshold
  dpmm_em_signal_threshold = opts.dpmm_em_signal_threshold
  dpmm_em_avoid_distance = opts.dpmm_em_avoid_distance
  dpmm_ur_square_size = opts.dpmm_ur_square_size
  dpmm_ur_delete_size = opts.dpmm_ur_delete_size
  ifs_multiplier = opts.ifs_multiplier
  ifs_min_matrix_threshold = opts.ifs_min_matrix_threshold


  ###############################################################################
  # Initialization
  ###############################################################################

  # Config data classes
  juicer_command = JuicerCommand()
  cooler_command = CoolerCommand()
  chromosome_sizes = ChromosomeSizes(organism)
  barcode_files = BarcodeFiles()
  exc_list = ExcList(organism, resolution)
  channel = Channel()

  ###############################################################################
  # Reading user's contact map
  ###############################################################################

  #chromosome ######## TODO
  #region ######### TODO

  # Check allowed chromosomes
  if(not chromosome):
    io_allowed_chromosomes = None
  else:
    io_allowed_chromosomes = [chromosome]

  # Initialize IO instance
  io_instance = IO(input_matrix, temporary_location, organism, cores, error_handler, chromosome_sizes, juicer_command, cooler_command,
                   input_resolution = resolution, allowed_chromosomes = io_allowed_chromosomes, input_file_type = input_type, seed = seed)

  # Read contact map
  contact_map = io_instance.read()

  # Update allowed chromosomes
  if(not chromosome):
    contact_map.update_valid_chromosome_list()
  else:
    contact_map.valid_chromosome_list = [chromosome]

  # Calculate all contact map initial statistics
  contact_map.calculate_all_statistics()


  ###############################################################################
  # Barcode
  ###############################################################################

  # Deprecated - Barcodes are deprecated in the current version

  # Verify barcode
  # barcode_instance = Barcode(cores, organism, contact_map, temporary_location, error_handler, barcode_files, juicer_command, cooler_command, seed = seed)
  # final_contact_map, final_loop_list = barcode_instance.main_guide()

  # Print matrix and loop list
  # if(final_contact_map and final_loop_list):
  #   io_instance.write(final_contact_map, output_matrix, output_format = output_type)
  #   io_instance.write_loop_list(final_loop_list, output_contacts)
  #   sys.exit(0)


  ###############################################################################
  # Preprocess
  ###############################################################################

  # Preprocess
  preprocess_instance = Preprocess(cores, contact_map, avoid_distance, error_handler, chromosome_sizes, exc_list,
                                   minimal_resolution = output_resolution, min_contig_removed_bins = pre_min_contig_removed_bins,
                                   remove_threshold = pre_remove_threshold, seed = seed)
  if(output_resolution < resolution):
    contact_map = preprocess_instance.convert_to_minimal_resolution(recalculate_statistics = True)
  elif(resolution < output_resolution):
    # TODO - Error
    pass
  preprocess_instance.check_sparsity()
  preprocess_instance.main_remove_blacklist(contact_map)
  preprocess_instance.main_void_statistics(contact_map)
  preprocess_instance.main_diagonal_homogeneic(contact_map)
  contact_map.calculate_all_statistics()


  ###############################################################################
  # ICA / SICA
  ###############################################################################

  # SICA
  sica_instance = Sica(cores, contact_map, avoid_distance, error_handler, channel, removed_dict = preprocess_instance.removed_dict,
                       pvalue_threshold = sica_pvalue_threshold, fitting_method = fitting_method, bottom_bin_ext_range = sica_bottom_bin_ext_range,
                       left_bin_ext_range = sica_left_bin_ext_range, right_bin_ext_range = sica_right_bin_ext_range, top_bin_ext_range = sica_top_bin_ext_range,
                       bonuscrosslb_range = sica_bonuscrosslb_range, bonuscross_range = sica_bonuscross_range, bonuslb_range = sica_bonuslb_range, seed = seed)
  sica_instance.main_existing_augmentation()
  sica_instance.main_calculate_distributions()
  sica_instance.main_diagonal_borderline()
  sica_instance.main_annotation_order()
  sica_instance.main_star_contacts(flag_first = True)
  contact_map.calculate_all_statistics()


  ###############################################################################
  # GOBA
  ###############################################################################

  # GOBA
  goba_instance = Goba(contact_map, sica_instance, error_handler, vertical_multiplier = goba_vertical_multiplier, ortogonal_multiplier = goba_ortogonal_multiplier, 
                       filling_frequency = goba_filling_frequency, banding_value_mult_range = goba_banding_value_mult_range,
                       banding_further_range = goba_banding_further_range, banding_frequency = goba_banding_frequency,
                       outing_value_mult_range = goba_outing_value_mult_range, outing_further_range = goba_outing_further_range,
                       outing_frequency = goba_outing_frequency, eppoch_resolution = goba_eppoch_resolution, eppoch_threshold = goba_eppoch_threshold, seed = seed)
  goba_instance.main_fill()
  goba_instance.main_banding()
  goba_instance.main_outing()
  contact_map.calculate_all_statistics()


  ###############################################################################
  # DPMM
  ###############################################################################

  # DPMM
  dpmm_instance = Dpmm(cores, contact_map, sica_instance, error_handler, random_degrade_range = dpmm_random_degrade_range,
                       degrade_multiplier = dpmm_degrade_multiplier, half_length_bin_interval = dpmm_half_length_bin_interval, 
                       value_range = dpmm_value_range, random_range = dpmm_random_range, iteration_multiplier = dpmm_iteration_multiplier,
                       em_significant_threshold = dpmm_em_significant_threshold, em_signal_threshold = dpmm_em_signal_threshold,
                       em_avoid_distance = dpmm_em_avoid_distance, ur_square_size = dpmm_ur_square_size, ur_delete_size = dpmm_ur_delete_size, seed = seed)
  dpmm_instance.main_em()
  #dpmm_instance.main_diagonal_em()
  dpmm_instance.introduce_shapes()
  contact_map.calculate_all_statistics()


  ###############################################################################
  # IFS
  ###############################################################################

  # IFS
  new_io_instance = IO(input_matrix, temporary_location, organism, cores, error_handler, chromosome_sizes, juicer_command, cooler_command,
                       input_resolution = output_resolution, input_file_type = input_type, seed = seed)
  ifs_instance = Ifs(contact_map, sica_instance, goba_instance, dpmm_instance, new_io_instance, output_contacts, output_matrix, output_type, error_handler, seed = seed)
  ifs_instance.main_calculate_ifs(min_to_zero = True)
  ifs_instance.main_fix_matrix(multiplier = ifs_multiplier, min_matrix_threshold = ifs_min_matrix_threshold)


  ###############################################################################
  # Termination
  ###############################################################################

  # Removing temporary file
  AuxiliaryFunctions.remove_folder_files(temporary_location)

  # Write final matrix and loop list
  # io_instance.write(contact_map, output_matrix, output_format = output_type)
  # io_instance.write_loop_list(loop_list, output_contacts)


