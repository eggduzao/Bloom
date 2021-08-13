from __future__ import print_function
"""
SICA Module
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
import random
import codecs
import warnings
import traceback
import subprocess
import configparser
import multiprocessing

# Internal
from bloom.contact_map import ContactMap
from bloom.util import ErrorHandler, AuxiliaryFunctions, Channel

# External
import numpy as np
import scipy
import scipy.stats as st

###################################################################################################
# Sica Class
###################################################################################################

class SicaDist():
  """This class represents TODO.

  *Keyword arguments:*

    - argument1 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.

    - argument2 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.
  """

  def __init__(self, contact_map, avoid_distance, channel_handler):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Fetching distance in bins given resolution
    self.A = avoid_distance
    self.T5 = channel_handler.tdict["t5"]
    self.T4 = channel_handler.tdict["t4"]
    self.T3 = channel_handler.tdict["t3"]
    self.T2 = channel_handler.tdict["t2"]
    self.T1 = channel_handler.tdict["t1"]
    self.C5 = channel_handler.cdict["c5"]
    self.C4 = channel_handler.cdict["c4"]
    self.C3 = channel_handler.cdict["c3"]
    self.C2 = channel_handler.cdict["c2"]
    self.C1 = channel_handler.cdict["c1"]
    self.O5 = channel_handler.odict["o5"]
    self.O4 = channel_handler.odict["o4"]
    self.O3 = channel_handler.odict["o3"]
    self.O2 = channel_handler.odict["o2"]
    self.O1 = channel_handler.odict["o1"]
    self.S = int(1e12)

    # Fixed distances bp
    self.Abp = (0, self.A)
    self.T5bp = (avoid_distance, self.T5)
    self.T4bp = (self.T5, self.T4)
    self.T3bp = (self.T4, self.T3)
    self.T2bp = (self.T3, self.T2)
    self.T1bp = (self.T2, self.T1)
    self.C5bp = (self.T1, self.C5)
    self.C4bp = (self.C5, self.C4)
    self.C3bp = (self.C4, self.C3)
    self.C2bp = (self.C3, self.C2)
    self.C1bp = (self.C2, self.C1)
    self.O5bp = (self.C1, self.O5)
    self.O4bp = (self.O5, self.O4)
    self.O3bp = (self.O4, self.O3)
    self.O2bp = (self.O3, self.O2)
    self.O1bp = (self.O2, self.O1)
    self.Sbp = (self.O1, int(1e12))

    # Fixed distances bin
    self.Abin = (contact_map.bp_to_bin(0), contact_map.bp_to_bin(self.A))
    self.T5bin = (contact_map.bp_to_bin(avoid_distance), contact_map.bp_to_bin(self.T5))
    self.T4bin = (contact_map.bp_to_bin(self.T5), contact_map.bp_to_bin(self.T4))
    self.T3bin = (contact_map.bp_to_bin(self.T4), contact_map.bp_to_bin(self.T3))
    self.T2bin = (contact_map.bp_to_bin(self.T3), contact_map.bp_to_bin(self.T2))
    self.T1bin = (contact_map.bp_to_bin(self.T2), contact_map.bp_to_bin(self.T1))
    self.C5bin = (contact_map.bp_to_bin(self.T1), contact_map.bp_to_bin(self.C5))
    self.C4bin = (contact_map.bp_to_bin(self.C5), contact_map.bp_to_bin(self.C4))
    self.C3bin = (contact_map.bp_to_bin(self.C4), contact_map.bp_to_bin(self.C3))
    self.C2bin = (contact_map.bp_to_bin(self.C3), contact_map.bp_to_bin(self.C2))
    self.C1bin = (contact_map.bp_to_bin(self.C2), contact_map.bp_to_bin(self.C1))
    self.O5bin = (contact_map.bp_to_bin(self.C1), contact_map.bp_to_bin(self.O5))
    self.O4bin = (contact_map.bp_to_bin(self.O5), contact_map.bp_to_bin(self.O4))
    self.O3bin = (contact_map.bp_to_bin(self.O4), contact_map.bp_to_bin(self.O3))
    self.O2bin = (contact_map.bp_to_bin(self.O3), contact_map.bp_to_bin(self.O2))
    self.O1bin = (contact_map.bp_to_bin(self.O2), contact_map.bp_to_bin(self.O1))
    self.Sbin = (contact_map.bp_to_bin(self.O1), contact_map.bp_to_bin(int(1e12)))

    # Distance list bp
    self.abp_dist_dict = dict([("a", self.Abp)])
    self.tbp_dist_dict = dict([("t5", self.T5bp), ("t4", self.T4bp), ("t3", self.T3bp), ("t2", self.T2bp), ("t1", self.T1bp)])
    self.cbp_dist_dict = dict([("c5", self.C5bp), ("c4", self.C4bp), ("c3", self.C3bp), ("c2", self.C2bp), ("c1", self.C1bp)])
    self.obp_dist_dict = dict([("o5", self.O5bp), ("o4", self.O4bp), ("o3", self.O3bp), ("o2", self.O2bp), ("o1", self.O1bp)])
    self.sbp_dist_dict = dict([("s", self.Sbp)])

    # Distance list bin
    self.abin_dist_dict = dict([("a", self.Abin)])
    self.tbin_dist_dict = dict([("t5", self.T5bin), ("t4", self.T4bin), ("t3", self.T3bin), ("t2", self.T2bin), ("t1", self.T1bin)])
    self.cbin_dist_dict = dict([("c5", self.C5bin), ("c4", self.C4bin), ("c3", self.C3bin), ("c2", self.C2bin), ("c1", self.C1bin)])
    self.obin_dist_dict = dict([("o5", self.O5bin), ("o4", self.O4bin), ("o3", self.O3bin), ("o2", self.O2bin), ("o1", self.O1bin)])
    self.sbin_dist_dict = dict([("s", self.Sbin)])

  def get_key_to_bin_dict(self, element, upper = False):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Creating new dictionary
    newdict = dict()
    for k in element.keys():
      if(upper):
        newkey = k.upper()
      else:
        newkey = k
      newdict[newkey] = True

    # Return objects
    return newdict

class Sica(): # TODO - Correct all places where A, T, C, O and S appear.
  """This class represents TODO.

  *Keyword arguments:*

    - argument1 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.

    - argument2 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.
  """

  def __init__(self, ncpu, contact_map, avoid_distance, removed_dict = None, pvalue_threshold = 0.95,
               bottom_bin_ext_range = [3,10], left_bin_ext_range = [3,10], right_bin_ext_range = [1,4], top_bin_ext_range = [1,4],
               bonuscrosslb_range = [0.25, 0.3], bonuscross_range = [0.1, 0.25], bonuslb_range = [0.1, 0.25], seed = None):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Seed
    if(seed):
      random.seed(seed)

    # Class objects
    self.contact_map = contact_map
    self.avoid_distance = avoid_distance
    self.pvalue_threshold = pvalue_threshold
    self.removed_dict = removed_dict
    self.seed = seed

    # Auxiliary objects
    self.bottom_bin_ext_range = bottom_bin_ext_range
    self.left_bin_ext_range = left_bin_ext_range
    self.right_bin_ext_range = right_bin_ext_range
    self.top_bin_ext_range = top_bin_ext_range
    self.bonuscrosslb_range = bonuscrosslb_range
    self.bonuscross_range = bonuscross_range
    self.bonuslb_range = bonuslb_range

    # Annotation dictionary
    self.annotation_dictionary = dict() # Same as contact_map matrix, but with an extra annotation flag:
    # R = Points removed because they fall into a 0 contig or blacklist.
    # A = Points to avoid because they fall in 0-avoid_distance
    # T1, T2, T3, T4, T5 = Tad hierarchy levels depending on point's distance to diagonal.
    # C1, C2, C3, C4, C5 = Compartment hierarchy levels depending on point's distance to diagonal.
    # O1, O2, O3, O4, O5 = Outter significant points not related to larger compartments.
    # S = Points farther from diagonal than the biggest compartment length (C1)
    # Upper case letters are important points. Lower case letters are less important points.

    # Auxiliary dictionaries
    self.distribution_dictionary = dict() # per chromosome / per SicaDist -> Contains all the matrix's signal within that specific SicaDist
    self.dist_to_diag_dictionary = dict() # per chromosome / per regular matrix key -> Manhattan distance to the diagonal
    self.pvalue_dictionary = dict() # per chromosome / per SicaDist -> Contains [name of the fitted distribution (FD), parameters of FD, value at pvalue_threshold (given FD)]

    # Keys of annotation dictionary based on contact_map's crescent value order
    self.annotation_dictionary_pvalue_order = dict() # per chromosome -> list of annotation dictionary keys (tuples) = [(a,b), (c,d)] ; where self.contact_map[chrom][(a,b)] < self.contact_map[chrom][(c,d)]
    
    # Dictionary with total number of each annotation mark (caps sensitive)
    self.annotation_dictionary_count = dict() # per chromosome / per annotation mark (r, R, a, A, t1, T1, etc.) -> total count

    # Auxiliary distributions
    self.distribution_list = [st.alpha, st.beta, st.burr, st.dgamma, st.dweibull, st.erlang, st.expon, st.exponpow, st.genexpon,
                              st.gilbrat, st.gumbel_r, st.invweibull, st.kstwobign, st.levy, st.ncx2, st.wald, st.weibull_min]

    # Auxiliary parameters
    self.ncpu = ncpu
    self.process_queue = []

    # Utilitary objects
    self.error_handler = ErrorHandler()
    self.channel_handler = Channel()
    self.dist_handler = SicaDist(contact_map, avoid_distance, self.channel_handler)


  #############################################################################
  # Existing Augmentation
  #############################################################################

  def main_existing_augmentation(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Iterating on valid chromosomes - Starring contacts
    for chromosome in self.contact_map.valid_chromosome_list:

      # Add histogram calculation job to queue
      #self.add_existing_augmentation(chromosome)
      self.existing_augmentation(chromosome)

    # Run histogram calculation jobs
    #self.run_existing_augmentation()

  def existing_augmentation(self, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Vector of elements to add
    elements_to_add = []
    twice_avoid_distance = 2 * self.avoid_distance

    # Iterating on matrix
    for key, value in self.contact_map.matrix[chromosome].items():

      # Key point
      key_row_bp = key[0]
      key_col_bp = key[1]

      # Bin is a valid peak # Heuristic = Augment values which are 2 * avoid_value
      if(abs(key_col_bp - key_row_bp) >= twice_avoid_distance and abs(key_col_bp - key_row_bp) <= self.dist_handler.C5):

        # Try to fetch row diagonal
        row_diag_count = 1
        try:
          row_diag_count = self.contact_map.matrix[chromosome][(key_row_bp, key_row_bp)] + 1
        except Exception:
          pass

        # Try to fetch col diagonal
        col_diag_count = 1
        try:
          col_diag_count = self.contact_map.matrix[chromosome][(key_col_bp, key_col_bp)] + 1
        except Exception:
          pass

        # Calculating additional value
        newvalue = value + (value * np.log((row_diag_count + col_diag_count)/2))
        elements_to_add.append((chromosome, key_row_bp, key_col_bp, newvalue))

    # Adding elements
    for element in elements_to_add:
      self.contact_map.set(element[0], element[1], element[2], element[3])
      
  def add_existing_augmentation(self, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Append job to queue
    self.process_queue.append((chromosome))

  def run_existing_augmentation(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Execute job queue
    pool = multiprocessing.Pool(self.ncpu)
    pool.starmap(self.existing_augmentation, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()

    # Clean queue
    pool = None
    self.process_queue = []
    gc.collect()


  #############################################################################
  # Annotation
  #############################################################################

  # Each region distance is fit into a distribution, then a p-value is calculated
  # and a threshold is set to mark a point as a peak if p-value >= threshold.
  # Then, depending on the distance from diagonal, annotate each point with
  # a annotation letter: R, A, O, Tx, Cx.

  def main_calculate_distributions(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Allowed distances
    dist_dict = {**self.dist_handler.abin_dist_dict, **self.dist_handler.tbin_dist_dict, **self.dist_handler.cbin_dist_dict,
                 **self.dist_handler.obin_dist_dict, **self.dist_handler.sbin_dist_dict}

    # Iterating on valid chromosomes - Calculate histograms
    for chromosome in self.contact_map.valid_chromosome_list:

      # Put chromosome in distribution_dictionary, annotation dictionary and dist_to_diag_dictionary
      self.distribution_dictionary[chromosome] = dict()
      self.annotation_dictionary[chromosome] = dict()
      self.dist_to_diag_dictionary[chromosome] = dict()

      # Add histogram calculation job to queue
      #self.add_calculate_histogram(chromosome, dist_dict)
      self.calculate_histogram(chromosome, dist_dict)

    # Run histogram calculation jobs
    #self.run_calculate_histogram()

    # Iterating on valid chromosomes - Calculate pvalues
    for chromosome in self.contact_map.valid_chromosome_list:

      # Put chromosome in pvalue_dictionary
      self.pvalue_dictionary[chromosome] = dict()

      # Iterating on SicaDist
      for skey, svalue in dist_dict.items():

        # Add p-value calculation job to queue
        #self.add_calculate_pvalues(chromosome, svalue)
        self.calculate_pvalues(chromosome, svalue)

    # Run p-value calculation jobs
    #self.run_calculate_pvalues()

  def calculate_histogram(self, chromosome, dist_dict):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Iterating on matrix
    for key, value in self.contact_map.matrix[chromosome].items():

      # Check distance to diagonal
      min_bin_key = self.contact_map.bp_to_bin(key[0])
      max_bin_key = self.contact_map.bp_to_bin(key[1])

      bin_key = (min_bin_key, max_bin_key)
      distance_to_diag = self.contact_map.bin_distance_from_diagonal_manhattan(bin_key)

      # Add distance to diagonal to dictionary
      self.dist_to_diag_dictionary[chromosome][key] = distance_to_diag

      # Default annotation - Outside any distance = super
      annotation = "s"

      # Attribute distance - Removed dict
      try:
        if(self.removed_dict[chromosome][bin_key[0]]):
          annotation = "r"
      except Exception:
        pass
      try:
        if(self.removed_dict[chromosome][bin_key[1]]):
          annotation = "r"
      except Exception:
        pass

      # Attribute distance - Sica dist dict
      if(annotation != "r"):

        # Iterating on SicaDist distances
        for skey, svalue in dist_dict.items():

          if(svalue[0] <= distance_to_diag < svalue[1]):
            annotation = skey
            try:
              self.distribution_dictionary[chromosome][svalue].append(value)
            except Exception:
              self.distribution_dictionary[chromosome][svalue] = [value]
            break

      # Put value in the annotation dictionary
      self.annotation_dictionary[chromosome][key] = annotation


  def add_calculate_histogram(self, chromosome, dist_dict):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Append job to queue
    self.process_queue.append((chromosome, dist_dict))

  def run_calculate_histogram(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Execute job queue
    pool = multiprocessing.Pool(self.ncpu)
    pool.starmap(self.calculate_histogram, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()

    # Clean queue
    pool = None
    self.process_queue = []
    gc.collect()

  def best_fit_distribution(self, data, bins = 100):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Histogram from original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    # Best parameters initialization
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf
    best_pvalue = 0.9

    # Estimate distribution parameters from data
    for distribution in self.distribution_list:

      # Try to fit the distribution
      try:

        # Ignore warnings from data that can't be fit
        with warnings.catch_warnings():
          warnings.filterwarnings('ignore')

          # Fit distribution to data
          params = distribution.fit(data)

          # Separate parts of parameters
          arg = params[:-2]
          loc = params[-2]
          scale = params[-1]

          # Calculate fitted PDF, error with fit in distribution and value at pvalue_threshold
          pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
          sse = np.sum(np.power(y - pdf, 2.0))
          value_at_pvalue = distribution.ppf(self.pvalue_threshold, *arg, loc=loc, scale=scale) if arg else distribution.ppf(self.pvalue_threshold, loc=loc, scale=scale)

          # Update best distribution
          if(best_sse > sse > 0):
            best_distribution = distribution
            best_params = params
            best_sse = sse
            best_pvalue = value_at_pvalue

      except Exception as e:
        # PASS - TODO WARNING - IF NO DIST CAN BE FIT, SEND ERROR
        pass

    return best_distribution.name, best_params, best_pvalue

  def calculate_pvalues(self, chromosome, sica_dist):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Parameters
    minimum_data_size = 30
    histogram_maximum_bins = 100
    histogram_below_factor = 0.2

    # Calculating best p-value given the current distribution
    try:
      data = self.distribution_dictionary[chromosome][sica_dist]
    except Exception:
      return 0
    #curr_bins = min(int(len(data)/5),100)
    #best_distribution, best_params, best_pvalue = self.best_fit_distribution(data, bins = curr_bins)
    #self.pvalue_dictionary[chromosome][sica_dist] = [best_distribution, best_params, best_pvalue]

    if(len(data) > minimum_data_size):
      # ------- Previous version --------
      # curr_bins = min(int(len(data) * histogram_below_factor), histogram_maximum_bins)
      # ------- Modfication valid for counts only!!! --------
      curr_bins = np.arange(np.min(data), np.max(data), 1)
      #
      best_distribution, best_params, best_pvalue = self.best_fit_distribution(data, bins = curr_bins)
      self.pvalue_dictionary[chromosome][sica_dist] = [best_distribution, best_params, best_pvalue]
    else:
      best_distribution = None
      best_params = None
      best_pvalue = 1
      self.pvalue_dictionary[chromosome][sica_dist] = [best_distribution, best_params, best_pvalue]

    # Do not calculate best p values for avoided
    #if(sica_dist == self.dist_handler.sica_dist_dict["a"]): return

    # Iterating on matrix to update annotation dictionary
    for key, value in self.contact_map.matrix[chromosome].items():

      # Add distance to diagonal to dictionary
      distance_to_diag = self.dist_to_diag_dictionary[chromosome][key]

      # Check if current bin is inside the sica dist
      if(sica_dist[0] <= distance_to_diag < sica_dist[1]):

        # Update annotation dictionary if value is bigger than or equal threshold value at p-value
        if(value >= best_pvalue):
          self.annotation_dictionary[chromosome][key] = self.annotation_dictionary[chromosome][key].upper()

  def add_calculate_pvalues(self, chromosome, sica_dist):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Append job to queue
    self.process_queue.append((chromosome, sica_dist))

  def run_calculate_pvalues(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Execute job queue
    pool = multiprocessing.Pool(self.ncpu)
    pool.starmap(self.calculate_pvalues, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()

    # Clean queue
    pool = None
    self.process_queue = []
    gc.collect()


  #############################################################################
  # Diagonal Borderline
  #############################################################################

  def main_diagonal_borderline(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Allowed distances
    dist_dict = {**self.dist_handler.tbin_dist_dict, **self.dist_handler.cbin_dist_dict}

    # Iterating on valid chromosomes - Starring contacts
    for chromosome in self.contact_map.valid_chromosome_list:

      # Add histogram calculation job to queue
      #self.add_diagonal_borderline(chromosome, dist_dict)
      self.diagonal_borderline(chromosome, dist_dict)

    # Run histogram calculation jobs
    #self.run_diagonal_borderline()

  def diagonal_borderline(self, chromosome, dist_dict): # Recursive version
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Vector of elements to add
    elements_to_add = []

    # Putting all significant keys in a list
    significant_diag_key_list = []

    # Iterating on matrix
    for key, value in self.contact_map.matrix[chromosome].items():

      # Check if value exists and it is significant
      try:
        if(self.annotation_dictionary[chromosome][key] != "A"):
          continue
      except Exception:
        continue

      # Adding significant diagonal
      dkey_bp = key[0]
      dkey_bin = self.contact_map.bp_to_bin(dkey_bp)
      significant_diag_key_list.append([dkey_bp, dkey_bin])

    # Iterating diagonal list
    for row in range(0, len(significant_diag_key_list) - 1):

      for col in range(row + 1, len(significant_diag_key_list)):

        # Expanded keys
        dkey_row = significant_diag_key_list[row]
        dkey_col = significant_diag_key_list[col]
        dkey_row_bp = dkey_row[0]
        dkey_row_bin = dkey_row[1]
        dkey_col_bp = dkey_col[0]
        dkey_col_bin = dkey_col[1]

        # If the distance is inside avoid region, continue
        if(abs(dkey_col_bin - dkey_row_bin) <= self.dist_handler.Abin[1]):
          continue

        # If row or column is in the removed dict, continue
        try:
          if(self.removed_dict[chromosome][dkey_row_bin]):
            continue
        except Exception:
          pass
        try:
          if(self.removed_dict[chromosome][dkey_col_bin]):
            continue
        except Exception:
          pass

        # Distance to diagonal
        bin_key = (dkey_row_bin, dkey_col_bin)
        distance_to_diag = self.contact_map.bin_distance_from_diagonal_manhattan(bin_key)

        # Iterating on SicaDist distances
        for skey, svalue in dist_dict.items():

          # Check if inside sica dist
          if(svalue[0] <= distance_to_diag < svalue[1]):

            # Update annotation dictionary
            bp_key = (dkey_row_bp, dkey_col_bp)
            self.annotation_dictionary[chromosome][bp_key] = skey.upper()

            # Update matrix
            value_1 = 0
            value_2 = 0
            try:
              value_1 = self.contact_map.matrix[chromosome][(dkey_row_bp, dkey_row_bp)]
            except Exception:
              pass
            try:
              value_2 = self.contact_map.matrix[chromosome][(dkey_col_bp, dkey_col_bp)]
            except Exception:
              pass
            value = ((value_1 + value_2) / 2) / np.sqrt(distance_to_diag)
            elements_to_add.append((chromosome, bp_key[0], bp_key[1], value))

    # Adding elements
    for element in elements_to_add:
      self.contact_map.set(element[0], element[1], element[2], element[3])

  """
  def diagonal_borderline(self, chromosome, dist_dict): # Linear version
    ""Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    ""

    # Vector of elements to add
    elements_to_add = []

    # Auxiliary elements
    row_bin = -1
    row_bp = -1

    # Iterating on matrix
    for d_bin in range(0, self.contact_map.total_1d_bins[chromosome]):

      # bin / bp operations
      d_bp = self.contact_map.bin_to_bp(d_bin)
      key = (d_bp, d_bp)

      # Check if value exists and it is significant
      try:
        if(not self.annotation_dictionary[chromosome][key].isupper()):
          continue
      except Exception:
        continue

      # If the row_bp have not been assigned yet, continue
      if(row_bp != -1):

        # If the distance is inside avoid region, continue
        if(abs(d_bin - row_bin) <= self.dist_handler.Abin[1]):
          continue

        # If row or column is in the removed dict, continue
        try:
          if(self.removed_dict[chromosome][d_bin]):
            continue
        except Exception:
          pass
        try:
          if(self.removed_dict[chromosome][row_bin]):
            continue
        except Exception:
          pass

        # Distance to diagonal
        bin_key = (row_bin, d_bin)
        distance_to_diag = self.contact_map.bin_distance_from_diagonal_manhattan(bin_key)

        # Iterating on SicaDist distances
        for skey, svalue in dist_dict.items():

          # Check if inside sica dist
          if(svalue[0] <= distance_to_diag < svalue[1]):

            # Update annotation dictionary
            bp_key = (row_bp, d_bp)
            self.annotation_dictionary[chromosome][bp_key] = skey.upper()

            # Update matrix
            value_1 = 0
            value_2 = 0
            try:
              value_1 = self.contact_map.matrix[chromosome][(d_bp, d_bp)]
            except Exception:
              pass
            try:
              value_2 = self.contact_map.matrix[chromosome][(row_bp, row_bp)]
            except Exception:
              pass
            value = ((value_1 + value_2) / 2) / distance_to_diag
            elements_to_add.append((chromosome, bp_key[0], bp_key[1], value))

      # Assign last diagonal search bp / bin to the next row bp / bin
      row_bp = d_bp
      row_bin = d_bin

    # Adding elements
    for element in elements_to_add:
      self.contact_map.add(element[0], element[1], element[2], element[3])
  """

  def add_diagonal_borderline(self, chromosome, dist_dict):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Append job to queue
    self.process_queue.append((chromosome, dist_dict))

  def run_diagonal_borderline(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Execute job queue
    pool = multiprocessing.Pool(self.ncpu)
    pool.starmap(self.diagonal_borderline, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()

    # Clean queue
    pool = None
    self.process_queue = []
    gc.collect()


  #############################################################################
  # Order Annotation by Contact Intensity
  #############################################################################

  def main_annotation_order(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Iterating on valid chromosomes - Starring contacts
    for chromosome in self.contact_map.valid_chromosome_list:

      # Add histogram calculation job to queue
      #self.add_annotation_order(chromosome)
      self.annotation_order(chromosome)

    # Run histogram calculation jobs
    #self.run_annotation_order()


  def annotation_order(self, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Initializing chromosome for annotation dict key list
    self.annotation_dictionary_pvalue_order[chromosome] = []
    self.annotation_dictionary_count[chromosome] = dict()

    # Iterating on original annotation dictionary
    for key, value in self.annotation_dictionary[chromosome].items():

      # Add key and contact value to annotation dict key list
      contact_value = self.contact_map.matrix[chromosome][key]
      self.annotation_dictionary_pvalue_order[chromosome].append(list(key) + [contact_value])

      # Counting total annotation marks of each type
      try:
        self.annotation_dictionary_count[chromosome][value] += 1
      except Exception:
        self.annotation_dictionary_count[chromosome][value] = 1

    # Sort the whole annotation dict key list in descending order by contact values
    self.annotation_dictionary_pvalue_order[chromosome] = sorted(self.annotation_dictionary_pvalue_order[chromosome], key = lambda x: x[2], reverse = True)



    #print("annotation_dictionary_pvalue_order ##################################################################")
    #for vec in self.annotation_dictionary_pvalue_order[chromosome]:
    #  print("Key " + ", ".join([str(e) for e in vec[:-1]]) + " / Value = " + str(vec[-1]))

    #print("/n annotation_dictionary_count ##################################################################")
    #for key, value in self.annotation_dictionary_count[chromosome].items():
    #  print("Key " + str(key) + " / Value = " + str(value))




  def add_annotation_order(self, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Append job to queue
    self.process_queue.append((chromosome))

  def run_annotation_order(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Execute job queue
    pool = multiprocessing.Pool(self.ncpu)
    pool.starmap(self.annotation_order, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()

    # Clean queue
    pool = None
    self.process_queue = []
    gc.collect()


  #############################################################################
  # Star Dictionaries
  #############################################################################

  def main_star_contacts(self, flag_first = True):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Iterating on valid chromosomes - Starring contacts
    for chromosome in self.contact_map.valid_chromosome_list:

      # Add histogram calculation job to queue
      #self.add_star_contacts(chromosome)
      self.star_contacts(chromosome, flag_first)

    # Run histogram calculation jobs
    #self.run_star_contacts()

  def star_contacts(self, chromosome, flag_first):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Vector of elements to add
    elements_to_add = []

    # Iterating on matrix
    for key, value in self.contact_map.matrix[chromosome].items():

      # Performing star algorithm
      self.simple_star(chromosome, key, value, elements_to_add, flag_first = flag_first)

    # Adding elements
    for element in elements_to_add:
      self.contact_map.add(element[0], element[1], element[2], element[3])

  def simple_star(self, chromosome, key, value, elements_to_add, flag_first = True):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Bin is a valid peak
    if(self.annotation_dictionary[chromosome][key].isupper() and self.annotation_dictionary[chromosome][key] not in ["A", "S"]):

      # Key point
      key_row = key[0]
      key_col = key[1]

      # Selecting lengths
      if(flag_first):
        bottom = 0
        left = 0
        right = 0
        top = 0
      else:
        bottom = random.randint(self.bottom_bin_ext_range[0], self.bottom_bin_ext_range[1])
        left = random.randint(self.left_bin_ext_range[0], self.left_bin_ext_range[1])
        right = random.randint(self.right_bin_ext_range[0], self.right_bin_ext_range[1])
        top = random.randint(self.top_bin_ext_range[0], self.top_bin_ext_range[1])

      # Iterating on point
      for i in range(-top, bottom + 1):
        for j in range(-left, right + 1):

          # Absolute i and j
          absi = abs(i)
          absj = abs(j)

          # If point is valid to be modified
          if(((i <= 0) and (j <= 0) and ((absi + absj) <= min(left, top))) or
             ((i <= 0) and (j >= 0) and ((absi + absj) <= min(right, top))) or
             ((i >= 0) and (j <= 0) and ((absi + absj) <= min(left, bottom))) or
             ((i >= 0) and (j >= 0) and ((absi + absj) <= min(right, bottom)))):

            # Decrease
            if(flag_first):
              base_value = float(value) # / float(1 + absi + absj)
            else:
              base_value = float(value) / float(2**(1 + np.e + absi + absj))

            # Bonuscrosslb
            bonuscrosslb = 0
            if(((i == 0) and (j <= 0)) or ((j == 0) and (i >= 0))):
              bonuscrosslb = random.uniform(self.bonuscrosslb_range[0], self.bonuscrosslb_range[1]) * value

            # Bonuscross
            bonuscross = 0
            if((i == 0) or (j == 0)):
              bonuscross = random.uniform(self.bonuscross_range[0], self.bonuscross_range[1]) * value

            # Bonuslb
            bonuslb = 0
            if((i >= 0) and (j <= 0)):
              bonuslb = random.uniform(self.bonuslb_range[0], self.bonuslb_range[1]) * value

            # Final score
            final_score = base_value + bonuscrosslb + bonuscross + bonuslb
            bpi = self.contact_map.bin_to_bp(i)
            bpj = self.contact_map.bin_to_bp(j)
            elements_to_add.append((chromosome, key_row + bpi, key_col + bpj, final_score))

  def add_star_contacts(self, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Append job to queue
    self.process_queue.append((chromosome))

  def run_star_contacts(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Execute job queue
    pool = multiprocessing.Pool(self.ncpu)
    pool.starmap(self.star_contacts, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()

    # Clean queue
    pool = None
    self.process_queue = []
    gc.collect()


