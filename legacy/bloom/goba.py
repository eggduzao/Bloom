from __future__ import print_function
"""
GOBA Module
===================
Placeholder.

Authors: Eduardo G. Gusmao.

"""

###################################################################################################
# Libraries
###################################################################################################

# Python
import gc
import random
import multiprocessing

# Internal
from bloom.util import AuxiliaryFunctions

# External
import numpy


###################################################################################################
# Goba Class
###################################################################################################

class Goba():
  """This class represents TODO.

  *Keyword arguments:*

    - argument1 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.

    - argument2 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.
  """

  def __init__(self, contact_map, sica_instance, error_handler, vertical_multiplier = [0.5, 0.75], ortogonal_multiplier = [0.1, 0.3], 
               filling_frequency = 0.5, banding_value_mult_range = [0.4, 0.6], banding_further_range = [0.90, 0.99], banding_frequency = 0.5,
               outing_value_mult_range = [0.3, 0.5], outing_further_range = [0.90, 0.99], outing_frequency = 0.34,
               eppoch_resolution = 100000, eppoch_threshold = 5, seed = None):
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
    self.sica_instance = sica_instance
    self.seed = seed

    # Auxiliary objects
    self.vertical_multiplier = vertical_multiplier
    self.ortogonal_multiplier = ortogonal_multiplier
    self.filling_frequency = filling_frequency
    self.banding_value_mult_range = banding_value_mult_range
    self.banding_further_range = banding_further_range
    self.banding_frequency = banding_frequency
    self.outing_value_mult_range = outing_value_mult_range
    self.outing_further_range = outing_further_range
    self.outing_frequency = outing_frequency

    # Eppoch auxiliary objects
    self.eppoch_resolution = eppoch_resolution
    self.eppoch_threshold = eppoch_threshold # Estimate of max constraint at T3.
    self.eppoch_contraint_dict = dict() # By chrom / by phase / by annotation -> total current count.
    self.eppoch_threshold_dict = dict() # By chrom / by annotation -> threshold.
    self.main_calculate_eppoch_threshold_dictionary()

    # Auxiliary parameters
    self.ncpu = self.sica_instance.ncpu
    self.process_queue = []

    # Utilitary objects
    self.error_handler = error_handler


  #############################################################################
  # Calculate Eppoch
  #############################################################################

  def main_calculate_eppoch_threshold_dictionary(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Iterating on valid chromosomes - Calculate histograms
    for chromosome in self.contact_map.valid_chromosome_list:

      # Add chromosome to eppoch list
      self.eppoch_threshold_dict[chromosome] = dict()

      # Add histogram calculation job to queue
      self.calculate_eppoch_threshold_dictionary(chromosome)

  def calculate_eppoch_threshold_dictionary(self, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Set default at T3
    self.eppoch_threshold_dict[chromosome]["T3"] = self.eppoch_threshold

    # Set values at T4 and T5
    counter = 1
    for annotation in ["T4", "T5"]:
      self.eppoch_threshold_dict[chromosome][annotation] = int(round(self.eppoch_threshold * (2**counter)))
      counter += 1

    # Set values at T2 and T1
    counter = 1
    for annotation in ["T2", "T1"]:
      self.eppoch_threshold_dict[chromosome][annotation] = int(round(self.eppoch_threshold / (2**counter)))
      counter += 1


  #############################################################################
  # Filling
  #############################################################################

  def main_fill(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Iterating on valid chromosomes - Calculate histograms
    for chromosome in self.contact_map.valid_chromosome_list:

      # Add chromosome to eppoch list
      self.eppoch_contraint_dict[chromosome] = dict()

      # Add histogram calculation job to queue
      #self.add_fill(chromosome)
      self.fill(chromosome)

    # Run histogram calculation jobs
    #self.run_fill()

  def set_eppoch_constraint(self, chromosome, key, annotation):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Phasing
    phase = int(AuxiliaryFunctions.floor_multiple(key[0], self.eppoch_resolution))

    # Updating eppoch constraint dict and evaluating threshold
    flag_eppoch = False
    try:
      self.eppoch_contraint_dict[chromosome][phase][annotation] += 1
      if(self.eppoch_contraint_dict[chromosome][phase][annotation] > self.eppoch_threshold_dict[chromosome][annotation]):
        flag_eppoch = True
    except Exception:
      try:
        self.eppoch_contraint_dict[chromosome][phase][annotation] = 1
        if(self.eppoch_contraint_dict[chromosome][phase][annotation] > self.eppoch_threshold_dict[chromosome][annotation]):
          flag_eppoch = True
      except Exception:
        self.eppoch_contraint_dict[chromosome][phase] = dict()
        self.eppoch_contraint_dict[chromosome][phase][annotation] = 1
        if(self.eppoch_contraint_dict[chromosome][phase][annotation] > self.eppoch_threshold_dict[chromosome][annotation]):
          flag_eppoch = True

    # Return objects
    return flag_eppoch

  def fill(self, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Vector of elements to add
    elements_to_add = []

    # Allowed fill
    allowed_fill_dict = self.sica_instance.dist_handler.get_key_to_bin_dict(self.sica_instance.dist_handler.tbin_dist_dict, upper = True)
    del allowed_fill_dict["T1"] # Check TODO
    del allowed_fill_dict["T2"] # Check TODO

    # Initialization of frequency flag
    frequency_flag_curr_count = 0
    frequency_flag_total_count = 0
    for key in allowed_fill_dict.keys():
      try:
        frequency_flag_total_count += self.sica_instance.annotation_dictionary_count[chromosome][key]
      except Exception:
        continue

    # Iterating on matrix
    # for key, value in self.contact_map.matrix[chromosome].items(): # OLD Method
    for keyv in self.sica_instance.annotation_dictionary_pvalue_order[chromosome]:

      # Initialization
      key = tuple(keyv[:-1])
      value = keyv[-1]
      log_value = numpy.log(value + 1)

      # Bin row and col
      brow = self.contact_map.bp_to_bin(key[0])
      bcol = self.contact_map.bp_to_bin(key[1])

      # Check if contact is a peak star
      try:
        ann = self.sica_instance.annotation_dictionary[chromosome][key]
        if(ann in ["T2", "T1"] and log_value > 0):
          self.contact_map.set(chromosome, key[0], key[1], log_value)
        allowed_fill_dict[ann]
        frequency_flag_curr_count += 1
      except Exception:
        continue

      # Frequency check
      if((frequency_flag_curr_count / frequency_flag_total_count) > self.filling_frequency):
        try:
          self.sica_instance.annotation_dictionary[chromosome][key] = self.sica_instance.annotation_dictionary[chromosome][key].lower()
          self.sica_instance.annotation_dictionary_count[chromosome][ann] -= 1
        except Exception:
          pass
        try:
          if(log_value > 0):
            self.contact_map.set(chromosome, key[0], key[1], log_value)
        except Exception:
          pass
        continue

      # Frequency check # OLD Method
      #freq_check = random.random()
      #if(freq_check > self.filling_frequency):
      #  try:
      #    self.sica_instance.annotation_dictionary[chromosome][key] = self.sica_instance.annotation_dictionary[chromosome][key].lower()
      #  except Exception:
      #    pass
      #  try:
      #    if(log_value > 0):
      #      self.contact_map.set(chromosome, key[0], key[1], log_value)
      #  except Exception:
      #    pass
      #  continue

      # Eppoch check
      if(self.set_eppoch_constraint(chromosome, key, ann)):
        try:
          self.sica_instance.annotation_dictionary[chromosome][key] = self.sica_instance.annotation_dictionary[chromosome][key].lower()
          self.sica_instance.annotation_dictionary_count[chromosome][ann] -= 1
        except Exception:
          pass
        try:
          if(log_value > 0):
            self.contact_map.set(chromosome, key[0], key[1], log_value)
        except Exception:
          pass
        continue

      # Retrospect star algorithm # Flag-fist must be False to retrospect
      self.sica_instance.simple_star(chromosome, key, value, elements_to_add, flag_first = False)

      # Check distance to diagonal
      try:
        distance_to_diag = self.sica_instance.self.dist_to_diag_dictionary[chromosome][key]
      except Exception:
        bin_key = (brow, bcol)
        distance_to_diag = self.contact_map.bin_distance_from_diagonal_manhattan(bin_key)

      # Basis value
      basis_value = value / numpy.sqrt(distance_to_diag + 1)
        
      # Iterating on rows
      for i in range(brow, bcol + 1):
      #for i in range(brow, bcol):

        # Iterating on cols
        for j in range(bcol, i - 1, -1):
        #for j in range(bcol, i, -1):

          # Multiplier
          if(i == j or i == brow or j == bcol):
            mult = random.uniform(self.vertical_multiplier[0], self.vertical_multiplier[1])
          else:
            mult = random.uniform(self.ortogonal_multiplier[0], self.ortogonal_multiplier[1])

          # Final value add
          final_value = basis_value * mult
          bpi = self.contact_map.bin_to_bp(i)
          bpj = self.contact_map.bin_to_bp(j)
          elements_to_add.append((chromosome, bpi, bpj, final_value))

    # Adding elements
    for element in elements_to_add:
      if(element[3] > 0):
        self.contact_map.add(element[0], element[1], element[2], element[3])

  def add_fill(self, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Append job to queue
    self.process_queue.append((chromosome))

  def run_fill(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Execute job queue
    pool = multiprocessing.Pool(self.ncpu)
    pool.starmap(self.fill, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()

    # Clean queue
    pool = None
    self.process_queue = []
    gc.collect()


  #############################################################################
  # Banding
  #############################################################################

  def main_banding(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Iterating on valid chromosomes - Calculate histograms
    for chromosome in self.contact_map.valid_chromosome_list:

      # Add histogram calculation job to queue
      #self.add_banding(chromosome)
      self.banding(chromosome)

    # Run histogram calculation jobs
    #self.run_banding()

  def banding(self, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Vector of elements to add
    elements_to_add = []

    # Allowed fill
    allowed_fill_dict = self.sica_instance.dist_handler.get_key_to_bin_dict(self.sica_instance.dist_handler.cbin_dist_dict, upper = True)

    # Columns to fill
    columns_to_fill = dict()

    # Initialization of frequency flag
    frequency_flag_curr_count = 0
    frequency_flag_total_count = 0
    for key in allowed_fill_dict.keys():
      try:
        frequency_flag_total_count += self.sica_instance.annotation_dictionary_count[chromosome][key]
      except Exception:
        continue

    # Iterating on matrix
    # for key, value in self.contact_map.matrix[chromosome].items(): # OLD Method
    for keyv in self.sica_instance.annotation_dictionary_pvalue_order[chromosome]:

      # Initialization
      key = tuple(keyv[:-1])
      value = keyv[-1]

      # Check if contact is a peak star
      try:
        ann = self.sica_instance.annotation_dictionary[chromosome][key]
        allowed_fill_dict[ann]
        frequency_flag_curr_count += 1
      except Exception:
        continue

      # Frequency check
      if(frequency_flag_curr_count / frequency_flag_total_count > self.banding_frequency):
        try:
          self.sica_instance.annotation_dictionary[chromosome][key] = self.sica_instance.annotation_dictionary[chromosome][key].lower()
          self.sica_instance.annotation_dictionary_count[chromosome][ann] -= 1
        except Exception:
          pass
        try:
          log_value = numpy.log(value + 1)
          if(log_value > 0):
            self.contact_map.set(chromosome, key[0], key[1], log_value)
        except Exception:
          pass
        continue

      # Frequency check # OLD Method
      #freq_check = random.random()
      #if(freq_check > self.banding_frequency):
      #  try:
      #    self.sica_instance.annotation_dictionary[chromosome][key] = self.sica_instance.annotation_dictionary[chromosome][key].lower()
      #  except Exception:
      #    pass
      #  try:
      #    log_value = numpy.log(value + 1)
      #    if(log_value > 0):
      #      self.contact_map.set(chromosome, key[0], key[1], log_value)
      #  except Exception:
      #    pass
      #  continue

      # Adding column to dictionary
      col = key[1]
      try:
        if(columns_to_fill[col] < value):
          columns_to_fill[col] = value
      except Exception:
        columns_to_fill[col] = value

    # Iterating on the column dictionary
    for col, value in columns_to_fill.items():

      # Value
      newvalue = value * random.uniform(self.banding_value_mult_range[0], self.banding_value_mult_range[1])

      # Iterating on rows
      for row in range(0, col + 1, self.contact_map.resolution):

        # Signal check
        try:
          self.contact_map.matrix[chromosome][(row, col)]
          continue
        except Exception:
          pass

        # Value
        newvalue = newvalue * random.uniform(self.banding_further_range[0], self.banding_further_range[1])
        elements_to_add.append((chromosome, row, col, newvalue))
      
    # Adding elements
    for element in elements_to_add:
      if(element[3] > 0):
        self.contact_map.add(element[0], element[1], element[2], element[3])

  def add_banding(self, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Append job to queue
    self.process_queue.append((chromosome))

  def run_banding(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Execute job queue
    pool = multiprocessing.Pool(self.ncpu)
    pool.starmap(self.banding, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()

    # Clean queue
    pool = None
    self.process_queue = []
    gc.collect()


  #############################################################################
  # Outing
  #############################################################################

  def main_outing(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Iterating on valid chromosomes - Calculate histograms
    for chromosome in self.contact_map.valid_chromosome_list:

      # Add histogram calculation job to queue
      #self.add_outing(chromosome)
      self.outing(chromosome)

    # Run histogram calculation jobs
    #self.run_outing()

  def outing(self, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Vector of elements to add
    elements_to_add = []

    # Allowed fill
    allowed_fill_dict = self.sica_instance.dist_handler.get_key_to_bin_dict(self.sica_instance.dist_handler.obin_dist_dict, upper = True)

    # Columns to fill
    rows_to_fill = dict()

    # Initialization of frequency flag
    frequency_flag_curr_count = 0
    frequency_flag_total_count = 0
    for key in allowed_fill_dict.keys():
      try:
        frequency_flag_total_count += self.sica_instance.annotation_dictionary_count[chromosome][key]
      except Exception:
        continue

    # Iterating on matrix
    # for key, value in self.contact_map.matrix[chromosome].items(): # OLD Method
    for keyv in self.sica_instance.annotation_dictionary_pvalue_order[chromosome]:

      # Initialization
      key = tuple(keyv[:-1])
      value = keyv[-1]

      # Check if contact is a peak star
      try:
        ann = self.sica_instance.annotation_dictionary[chromosome][key]
        allowed_fill_dict[ann]
        frequency_flag_curr_count += 1
      except Exception:
        continue

      # Frequency check
      if(frequency_flag_curr_count / frequency_flag_total_count > self.outing_frequency):
        try:
          self.sica_instance.annotation_dictionary[chromosome][key] = self.sica_instance.annotation_dictionary[chromosome][key].lower()
          self.sica_instance.annotation_dictionary_count[chromosome][ann] -= 1
        except Exception:
          pass
        try:
          log_value = numpy.log(value + 1)
          if(log_value > 0):
            self.contact_map.set(chromosome, key[0], key[1], log_value)
        except Exception:
          pass
        continue

      # Frequency check # TODO
      #freq_check = random.random()
      #if(freq_check > self.outing_frequency):
      #  try:
      #    self.sica_instance.annotation_dictionary[chromosome][key] = self.sica_instance.annotation_dictionary[chromosome][key].lower()
      #  except Exception:
      #    pass
      #  try:
      #    log_value = numpy.log(value + 1)
      #    if(log_value > 0):
      #      self.contact_map.set(chromosome, key[0], key[1], log_value)
      #  except Exception:
      #    pass
      #  continue

      # Adding row to dictionary
      row = key[0]
      try:
        if(rows_to_fill[row] < value):
          rows_to_fill[row] = value
      except Exception:
        rows_to_fill[row] = value

    # Iterating on the column dictionary
    for row, value in rows_to_fill.items():

      # Value
      newvalue = value * random.uniform(self.outing_value_mult_range[0], self.outing_value_mult_range[1])

      # Iterating on rows
      for col in range(row, self.contact_map.chromosome_sizes.chromosome_sizes_dictionary[chromosome], self.contact_map.resolution):

        # Signal check
        try:
          self.contact_map.matrix[chromosome][(row, col)]
          continue
        except Exception:
          pass

        # Value
        newvalue = newvalue * random.uniform(self.outing_further_range[0], self.outing_further_range[1])
        elements_to_add.append((chromosome, row, col, newvalue))

    # Adding elements
    for element in elements_to_add:
      if(element[3] > 0):
        self.contact_map.add(element[0], element[1], element[2], element[3])

  def add_outing(self, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Append job to queue
    self.process_queue.append((chromosome))

  def run_outing(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Execute job queue
    pool = multiprocessing.Pool(self.ncpu)
    pool.starmap(self.outing, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()

    # Clean queue
    pool = None
    self.process_queue = []
    gc.collect()


  #############################################################################
  # Writing
  #############################################################################

  def write_tads(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Write the TADs based on the apexDict
    pass # Future TODO

  def write_compartments(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Write compartments based on the compDict
    pass # Future TODO


  #############################################################################
  # Delineating
  #############################################################################

  def delineate_tads(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Delineate TADs according to random, distance to diagonal and distance to important points
    pass # Future TODO

  def delineate_compartments(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Delineate compartments according to random, distance to diagonal and distance to important points
    pass # Future TODO


  #############################################################################
  # 2D Shearing
  #############################################################################

  def unshear(self, D, g):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
   
    # Real and imaginary parts
    D1, D2 = D[..., 0], D[..., 1]
    g1, g2 = g[0], g[1]
    a, b = D1 - g1, D2 - g2
    c, d = (1.0 - g1*D1 - g2*D2), g2*D1 - g1*D2

    # Shear out division
    out = numpy.empty_like(D)
    den = c**2 + d**2
    out[..., 0] = (a*c + b*d)/den
    out[..., 1] = (b*c - a*d)/den

    # Return objects
    return out

  def draw_g_1d_weak_shear(self, D, phi, label):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # 1D with Gaussian (canonical)
    Lam = 0.0  
    eta = 0.0
    for i, ph in enumerate(phi):
      index = numpy.nonzero(label == i)
      Lam += len(index[0])/ph
      eta += numpy.sum(D[index]/ph)
    var = 1./Lam
    mu = eta*var

    # Return objects
    return numpy.random.normal(loc=mu, scale=numpy.sqrt(var))

  def draw_g_2d_weak_shear(self, D, phi, label):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # 2D with Gaussian (canonical)
    Lam = 0.0  
    eta = 0.0
    for i, ph in enumerate(phi):
      index = numpy.nonzero(label == i)
      Lam += len(index[0])/ph
      eta += numpy.sum(D[index]/ph, axis=0)
    var = 1./Lam
    mu = eta*var

    # Return objects
    return numpy.random.multivariate_normal(mean=mu, cov=var*numpy.eye(2))


###################################################################################################
# Linear 1D Shear Class
###################################################################################################

class Linear1DShear():
  """This class represents TODO.

  *Keyword arguments:*

    - argument1 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.

    - argument2 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.
  """

  def __init__(self, g):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    self.g = g

  def init(self, D):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    self.g = numpy.mean(D)

  def __call__(self, D):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    return D - self.g

  def unmanip(self, D):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    return D + self.g

  def update(self, D, phi, label, prior):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    self.g = draw_g_1d_weak_shear(D, phi, label)


###################################################################################################
# Weak Shear Class
###################################################################################################

class WeakShear():
  """This class represents TODO.

  *Keyword arguments:*

    - argument1 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.

    - argument2 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.
  """

  def __init__(self, g):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    self.g = g

  def init(self, D):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    self.g = numpy.mean(D, axis=0)

  def __call__(self, D):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    return D - self.g

  def unmanip(self, D):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    return D + self.g

  def update(self, D, phi, label, prior):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    self.g = draw_g_2d_weak_shear(D, phi, label)


###################################################################################################
# Shear Class
###################################################################################################

class Shear():
  """This class represents TODO.

  *Keyword arguments:*

    - argument1 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.

    - argument2 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.
  """

  def __init__(self, g):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    self.g = g
    self.Nproposals = 0
    self.Nacceptances = 0

  def init(self, D):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    self.g = numpy.mean(D, axis=0)

  def __call__(self, D):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    return unshear(D, self.g)

  def unmanip(self, D):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    return unshear(D, -self.g)

  def update(self, D, phi, label, prior):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    prop_g = numpy.random.multivariate_normal(mean=self.g, cov=numpy.eye(2)*0.003**2)
    current_e_int = unshear(D, self.g)
    prop_e_int = unshear(D, prop_g)
    current_lnlike = 0.0
    prop_lnlike = 0.0
    for i, ph in enumerate(phi):
      index = label == i
      current_lnlike += prior.lnlikelihood(current_e_int[index], ph)
      prop_lnlike += prior.lnlikelihood(prop_e_int[index], ph)

    if prop_lnlike > current_lnlike:
      self.g = prop_g
      self.Nacceptances += 1
    else:
      u = numpy.random.uniform()
      if u < numpy.exp(prop_lnlike - current_lnlike):
        self.g = prop_g
        self.Nacceptances += 1
        self.Nproposals += 1


