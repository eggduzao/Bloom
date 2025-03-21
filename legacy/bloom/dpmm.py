from __future__ import print_function
"""
DPMM Module
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


# External
import numpy


###################################################################################################
# Dpmm Class
###################################################################################################

class Dpmm():
  """This class represents TODO.

  *Keyword arguments:*

    - argument1 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.

    - argument2 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.
  """

  def __init__(self, ncpu, contact_map, sica_instance, error_handler, random_degrade_range = [0.01, 0.02], degrade_multiplier = 0.05,
               half_length_bin_interval = [1, 5], value_range = [10e-4, 10e-3], random_range = [10e-8, 10e-7], iteration_multiplier = 1000,
               em_significant_threshold = 10, em_signal_threshold = 1.0, em_avoid_distance = 5, ur_square_size = 1000000, ur_delete_size = 10000000, seed = None):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Seed
    if(seed):
      random.seed(seed)

    # Main objects
    self.contact_map = contact_map

    # Degrade objects
    self.sica_instance = sica_instance
    self.random_degrade_range = random_degrade_range
    self.degrade_multiplier = degrade_multiplier

    # Shape objects
    self.half_length_bin_interval = half_length_bin_interval
    self.value_range = value_range
    self.random_range = random_range
    self.iteration_multiplier = iteration_multiplier

    # E-M objects
    self.em_significant_threshold = em_significant_threshold
    self.em_signal_threshold = em_signal_threshold
    self.em_avoid_distance = int(em_avoid_distance * self.contact_map.resolution)
    self.ur_square_size = ur_square_size
    self.ur_delete_size = ur_delete_size
    self.em_dictionary = dict() # per chromosome / per regular key -> average of upper-right square

    # Auxiliary parameters
    self.seed = seed
    self.ncpu = ncpu
    self.process_queue = []

    # Utilitary objects
    self.error_handler = error_handler
    self.sica_dist_handler = self.sica_instance.dist_handler

  #############################################################################
  # Expectation Maximization
  #############################################################################

  def main_em(self):
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

      self.em_dictionary[chromosome] = dict()

      # Add introduce_squares to the queue
      #self.add_expectation(chromosome)
      self.expectation(chromosome)

    # Run introduce squares
    #self.run_expectation()

    # Iterating on valid chromosomes
    for chromosome in valid_chromosome_list:

      # Add introduce_squares to the queue
      #self.add_maximization(chromosome)
      self.maximization(chromosome)

    # Run introduce squares
    #self.run_maximization()

  def expectation(self, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Allowed range
    allowed_dict = ["A", "T5"]

    # Iterating on matrix
    for key, value in self.sica_instance.annotation_dictionary[chromosome].items():

      # Coordinates
      row_bp = key[0]
      col_bp = key[1]

      # Check if diagonal and significant
      if(value in allowed_dict):

        # Initialization of parameters
        total_significant = 0
        value_summation = 0.0
        total_values = 0

        # New coordinates
        new_row_bp = row_bp - self.em_avoid_distance
        new_col_bp = col_bp + self.em_avoid_distance

        # Iteration on UR square rows
        for row in range(new_row_bp, new_row_bp - self.ur_square_size, -self.contact_map.resolution):

          # Limit check
          if(row < 0): break

          # Iteration on UR square cols
          for col in range(new_col_bp, new_col_bp + self.ur_square_size, self.contact_map.resolution):

            # Try to fetch contact value to summation
            try:
              contact_value = self.contact_map.matrix[chromosome][(row, col)]
              if(contact_value > 0):
                value_summation += contact_value
                total_values += 1
            except Exception:
              pass

            # Try to fetch significance
            try:
              sig_value = self.sica_instance.annotation_dictionary[chromosome][(row, col)]
              if(sig_value.isupper()):
                total_significant += 1
            except Exception:
              pass

        # Calculate average value
        try:
          average_value = value_summation / total_values
        except Exception:
          average_value = 0.0
        self.em_dictionary[chromosome][key] = [average_value, total_significant, value]

  def maximization(self, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Iterating on the EM dictionary
    for key, value in self.em_dictionary[chromosome].items():

      # Coordinates and values
      row_bp = key[0]
      col_bp = key[1]
      average_value = value[0]
      total_significant = value[1]

      # Check threshold
      if(average_value > self.em_signal_threshold or total_significant > self.em_significant_threshold):
        continue

      # New coordinates
      new_row_bp = row_bp - self.em_avoid_distance
      new_col_bp = col_bp + self.em_avoid_distance

      # Iteration on UR square rows
      for row in range(new_row_bp, new_row_bp - self.ur_delete_size, -self.contact_map.resolution):

        # Limit check
        if(row < 0): break

        # Iteration on UR square cols
        for col in range(new_col_bp, new_col_bp + self.ur_delete_size, self.contact_map.resolution):

          # Speed check
          try:
            new_value = numpy.log2(self.contact_map.matrix[chromosome][(row, col)] + 1)
          except Exception:
            continue
      
          # Try assuaging
          try:
            if(new_value <= 0):
              del self.contact_map.matrix[chromosome][(row, col)]
            else:
              self.contact_map.matrix[chromosome][(row, col)] = new_value
          except Exception:
            continue

          # Try assuaging
          try:
            self.sica_instance.annotation_dictionary[chromosome][(row, col)] = self.sica_instance.annotation_dictionary[chromosome][(row, col)].lower()
          except Exception:
            continue

  def add_expectation(self, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Append job to queue
    self.process_queue.append((chromosome))

  def add_maximization(self, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Append job to queue
    self.process_queue.append((chromosome))

  def run_expectation(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    
    # Execute job queue
    pool = multiprocessing.Pool(self.ncpu)
    pool.starmap(self.expectation, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()

    # Clean queue
    pool = None
    self.process_queue = []
    gc.collect()

  def run_maximization(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    
    # Execute job queue
    pool = multiprocessing.Pool(self.ncpu)
    pool.starmap(self.maximization, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()

    # Clean queue
    pool = None
    self.process_queue = []
    gc.collect()


  #############################################################################
  # Diagonal Degrade
  #############################################################################

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
      #self.add_degrade(self.contact_map, chromosome)
      self.degrade(self.contact_map, chromosome)

    # Run introduce squares
    #self.run_degrade()

  def degrade(self, contact_map, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    # Vector of elements to add
    elements_to_add = []

    # Get highest matrix value
    #highest_value = contact_map.max_value[chromosome]
    avoid_numpy_array = numpy.array(self.sica_instance.distribution_dictionary[chromosome][self.sica_dist_handler.Abin])
    average_avoided_value = numpy.mean(avoid_numpy_array)

    # Iterate on the rows of this chromosome's contact map
    for row in range(0, contact_map.total_1d_bins[chromosome]):

      # Calculate row's random multiplier and exponential multiplier
      row_random_r = (random.uniform(self.random_degrade_range[0] * average_avoided_value, self.random_degrade_range[1] * average_avoided_value) + average_avoided_value)
      row_expone_l = self.degrade_multiplier * average_avoided_value

      # Iterate on columns backwards
      counter = 1
      avoid_distance_in_bins = self.contact_map.bp_to_bin(self.sica_instance.avoid_distance)
      for col in range(row + avoid_distance_in_bins, row - 1, -1):

        # Calculate value to add in the matrix
        value_to_add = row_random_r + ((1 + row_expone_l) * counter)
        bprow = self.contact_map.bin_to_bp(row)
        bpcol = self.contact_map.bin_to_bp(col)
        elements_to_add.append((chromosome, bprow, bpcol, value_to_add))

        # Update counter
        counter += 1

    # Adding elements
    for element in elements_to_add:
      if(element[3] > 0):
        self.contact_map.add(element[0], element[1], element[2], element[3])

  def add_degrade(self, contact_map, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Append job to queue
    self.process_queue.append((genome_id, contact_map, chromosome))

  def run_degrade(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    
    # Execute job queue
    pool = multiprocessing.Pool(self.ncpu)
    pool.starmap(self.degrade, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()

    # Clean queue
    pool = None
    self.process_queue = []
    gc.collect()


  #############################################################################
  # Diagonal Expectation Maximization
  #############################################################################

  def main_diagonal_em(self):
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
      #self.add_diagonal_em(self.contact_map, chromosome)
      self.diagonal_em(self.contact_map, chromosome)

    # Run introduce squares
    #self.run_diagonal_em()

  def diagonal_em(self, contact_map, chromosome):
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

      # Expectation
      #if(value > 1):
      #  newvalue = numpy.log2(value)
      #elif(value > 0):
      #  newvalue = numpy.exp(value)
      #else:
      #  newvalue = random.uniform(self.random_degrade_range[0], self.random_degrade_range[1])
      if(value > 0):
        newvalue = numpy.log2(value + 1)
      else:
        continue

      # Fix calculus
      elements_to_add.append((chromosome, key[0], key[1], newvalue))

    # Maximization
    for element in elements_to_add:
      if(element[3] > 0):
        self.contact_map.set(element[0], element[1], element[2], element[3])

  def add_diagonal_em(self, contact_map, chromosome):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Append job to queue
    self.process_queue.append((genome_id, contact_map, chromosome))

  def run_diagonal_em(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    
    # Execute job queue
    pool = multiprocessing.Pool(self.ncpu)
    pool.starmap(self.diagonal_em, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()

    # Clean queue
    pool = None
    self.process_queue = []
    gc.collect()


  #############################################################################
  # Shapes
  #############################################################################

  def introduce_shapes(self):
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

      # Get number of iterations based on the size of the matrix
      iterations = int(self.contact_map.total_bins_triangle[chromosome] * self.iteration_multiplier)

      # Add introduce_squares to the queue
      #self.add_introduce_squares(self.contact_map, chromosome, iterations)
      self.introduce_squares(self.contact_map, chromosome, iterations)

    # Run introduce squares
    #self.run_introduce_squares()

    # Iterating on valid chromosomes
    for chromosome in valid_chromosome_list:

      # Get number of iterations based on the size of the matrix
      iterations = int(self.contact_map.total_bins_triangle[chromosome] * self.iteration_multiplier)

      # Add introduce_circles to the queue
      #self.add_introduce_circles(self.contact_map, chromosome, iterations)
      self.introduce_circles(self.contact_map, chromosome, iterations)

    # Run introduce circles
    #self.run_introduce_circles()

  def introduce_squares(self, contact_map, chromosome, iterations):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Maximum bp
    maximum_bp = contact_map.total_1d_bp[chromosome]

    # Performing the total number of iterations
    for main_iteration in range(0, iterations):

      # Square middle point
      chosen_length = random.randint(self.half_length_bin_interval[0], self.half_length_bin_interval[1]) * contact_map.resolution
      middle_bp_i = random.randrange(0, maximum_bp + 1, contact_map.resolution)
      middle_bp_j = random.randrange(0, maximum_bp + 1, contact_map.resolution)

      # Base value to add
      base_value = random.uniform(self.value_range[0], self.value_range[1])

      # Add a square
      for row in range(middle_bp_i - chosen_length, middle_bp_i + chosen_length + 1, contact_map.resolution):
        for col in range(middle_bp_j - chosen_length, middle_bp_j + chosen_length + 1, contact_map.resolution):

          # Verify if row and col are valid
          if((row > col) or (row < 0) or (col < 0) or (row > maximum_bp) or (col > maximum_bp)):
            continue

          # Value to add
          value_to_add = base_value + random.uniform(self.random_range[0], self.random_range[1])
          if(value_to_add > 0):
            contact_map.add(chromosome, row, col, value_to_add)

  def add_introduce_squares(self, contact_map, chromosome, iterations):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Append job to queue
    self.process_queue.append((genome_id, contact_map, chromosome, iterations))

  def run_introduce_squares(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    
    # Execute job queue
    pool = multiprocessing.Pool(self.ncpu)
    pool.starmap(self.introduce_squares, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()

    # Clean queue
    pool = None
    self.process_queue = []
    gc.collect()

  def introduce_circles(self, contact_map, chromosome, iterations):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Maximum bp
    maximum_bp = contact_map.total_1d_bp[chromosome]
  
    # Performing the total number of iterations
    for main_iteration in range(0, iterations):

      # Square middle point
      base_chosen_length = random.randint(self.half_length_bin_interval[0], self.half_length_bin_interval[1])
      chosen_length = base_chosen_length * contact_map.resolution
      middle_bp_i = random.randrange(0, maximum_bp + 1, contact_map.resolution)
      middle_bp_j = random.randrange(0, maximum_bp + 1, contact_map.resolution)

      # Base value to add
      base_value = random.uniform(self.value_range[0], self.value_range[1])

      # Add a circle
      counterI = - base_chosen_length
      counterJ = - base_chosen_length
      for row in range(middle_bp_i - chosen_length, middle_bp_i + chosen_length + 1, contact_map.resolution):
        for col in range(middle_bp_j - chosen_length, middle_bp_j + chosen_length + 1, contact_map.resolution):

          # Circle constraint
          if((abs(counterI) + abs(counterJ)) > base_chosen_length):
            continue

          # Verify if row and col are valid
          if((row > col) or (row < 0) or (col < 0) or (row > maximum_bp) or (col > maximum_bp)):
            continue

          # Value to add
          value_to_add = base_value + random.uniform(self.random_range[0], self.random_range[1])
          if(value_to_add > 0):
            contact_map.add(chromosome, row, col, value_to_add)

          # Updating counter j
          counterJ += 1

          # Updating counter i
        counterJ += 0
        counterI += 1

  def add_introduce_circles(self, contact_map, chromosome, iterations):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Append job to queue
    self.process_queue.append((genome_id, contact_map, chromosome, iterations))

  def run_introduce_circles(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    
    # Execute job queue
    pool = multiprocessing.Pool(self.ncpu)
    pool.starmap(self.introduce_circles, [arguments for arguments in self.process_queue])
    pool.close()
    pool.join()

    # Clean queue
    pool = None
    self.process_queue = []
    gc.collect()

  """
  introduce_shapes(self, chromosome, diag_dist_scale, neighbor_dist_scale, max_neighbors, diag_dist_rand_range = [0.0, 0.1], neighbor_dist_rand_range = [0.0, 0.1])
    
    # Initialization
    star_score_threshold = self.matrix.get_sparsity_weighted_sum(chrom) # TODO - Check for a better threshold

    # Iterate through matrix
    for key in self.matrix.keys():

    # Check chromosome
    kk = key.split(":")
    chrom = kk[0]
    if(chrom != chromosome): continue

    # Initialization
    p1 = int(kk[1])
    p2 = int(kk[2])
    star_score_to_add = self.matrix.get_sparsity_weighted_sum(chrom) # TODO - Check for a better value to add

    # What to do with the diagonal?

    # diag_dist_scale = a number that is going to be divided by the distance to the diagonal. The closest to the diagonal, the higher the value to add in the star

    # neighbor_dist_scale = a number to be divided by the distance to the neighbor. The farther the neighbor, the less signal to add.

    # max_neighbors = maximum 1D neighbor distance to sum to have the value to add
  """


###################################################################################################
# DPMM Main Class
###################################################################################################

class DPMM():
  """This class represents TODO.

  *Keyword arguments:*

    - argument1 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.

    - argument2 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.
  """

  def __init__(self, prior, alpha, D, manip=None, phi=None, label=None):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Main objects
    self.prior = prior
    self.alpha = alpha
    self._D = D  # data
    if manip is None:
      manip = NullManip()
    self.manip = manip

    # Auxiliary latency
    self._initD()
    self.manip.init(self.D)
    self.n = len(self.D)

    # Initialize r_i array
    self.p = self.alpha * self.prior.pred(self.mD)[:, numpy.newaxis]

    # Dirichlet parameterization
    if phi is None:
      self.init_phi()
    else:
      self.phi = phi
      self.label = label
      self.nphi = [numpy.sum(label == i) for i in xrange(label.max())]

  def init_phi(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Parameter initialization
    self.label = numpy.zeros((self.n), dtype=int)
    self.phi = []
    self.nphi = []
    for i in xrange(self.n):
      self.update_c_i(i)
    self.update_phi()

  @property
  def mD(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Latent update
    if self.manip_needs_update:
      self._mD = self.manip(self.D)
      self.manip_needs_update = False
    return self._mD

  def _initD(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Latent vector
    if isinstance(self._D, PseudoMarginalData):
      self.D = numpy.mean(self._D.data, axis=1)
    else:
      self.D = self._D
    self.manip_needs_update = True

  def draw_new_label(self, i):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Do not do yield explicitely
    picked = pick_discrete(self.p[i]*numpy.append([1], self.nphi)) - 1
    return picked

  def del_c_i(self, i):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Decrement mixture instance
    label = self.label[i]
    self.nphi[label] -= 1

    # If mix is deleted, delete params
    if self.nphi[label] == 0:
      del self.phi[label]
      del self.nphi[label]
      self.label[self.label >= label] -= 1
      self.p = numpy.delete(self.p, label+1, axis=1)

  def update_c_i(self, i):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    label = self.draw_new_label(i)

    # Draw
    if label == -1:
      new_phi = self.prior.post(self.mD[i]).sample()
      self.phi.append(new_phi)
      self.nphi.append(1)
      self.label[i] = len(self.phi)-1
      self.p = numpy.append(self.p, numpy.zeros((self.n, 1), dtype=float), axis=1)
      self.p[i+1:, -1] = self.prior.like1(self.mD[i+1:], new_phi)
    else:
      self.label[i] = label
      self.nphi[label] += 1

  def update_c(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Update drawing
    for i in xrange(self.n):
      self.del_c_i(i)
      self.update_c_i(i)

  def update_phi(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Update parameter
    tot = 0
    for i in xrange(len(self.phi)):
      index = self.label == i
      tot += sum(index)
      data = self.mD[index]
      new_phi = self.prior.post(data).sample()
      self.phi[i] = new_phi
    self.p[:, 1:] = self.prior.like1(self.mD[:, numpy.newaxis], numpy.array(self.phi))

  def update_latent_data(self):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Iteration to calculate weights -> selecting a representative sample
    if isinstance(self._D, PseudoMarginalData):
      for i, ph in enumerate(self.phi):

        index = numpy.nonzero(self.label == i)[0]
        data = self._D[index]
        
        ps = self.prior.like1(self.manip(data.data), ph) / data.interim_prior
        ps /= numpy.sum(ps, axis=1)[:, numpy.newaxis]

        for j, p in enumerate(ps):
          self.D[index[j]] = data.data[j, pick_discrete(p)]

      self.p[:, 0] = self.alpha * self.prior.pred(self.mD)
      self.manip_needs_update = True
    else:
      pass # TODO - Report

  def update(self, n=1):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # General update
    for j in xrange(n):
      self.update_c()
      self.update_latent_data()
      self.update_phi()
      self.manip.update(self.D, self.phi, self.label, self.prior)
      self.manip_needs_update = True


###################################################################################################
# GaussND Class
###################################################################################################

class GaussND():
  """This class represents TODO.

  *Keyword arguments:*

    - argument1 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.

    - argument2 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.
  """

  def __init__(self, mu, Sig):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # GND Parameters
    self.mu = numpy.atleast_1d(mu)
    self.Sig = numpy.atleast_2d(Sig)
    self.d = len(self.mu)

  def cond(self, x):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Params of cond
    fixed = numpy.nonzero([x_ is not None for x_ in x])
    nonfixed = numpy.nonzero([x_ is None for x_ in x])
    mu1 = self.mu[nonfixed]
    mu2 = self.mu[fixed]
    Sig11 = self.Sig[nonfixed, nonfixed]
    Sig12 = self.Sig[fixed, nonfixed]
    Sig22 = self.Sig[fixed, fixed]

    # Calculation of cond
    new_mu = mu1 + numpy.dot(Sig12, numpy.dot(numpy.linalg.inv(Sig22), x[fixed[0]] - mu2))
    new_Sig = Sig11 - numpy.dot(Sig12, numpy.dot(numpy.linalg.inv(Sig22), Sig12.T))

    # Return object
    return GaussND(new_mu, new_Sig)

  def sample(self, size=None):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Sample drawn as a MN
    if self.d == 1:
      return numpy.random.normal(self.mu, scale=numpy.sqrt(self.Sig), size=size)
    else:
      return numpy.random.multivariate_normal(self.mu, self.Sig, size=size)


###################################################################################################
# GMM Class
###################################################################################################

class GMM():
  """This class represents TODO.

  *Keyword arguments:*

    - argument1 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.

    - argument2 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.
  """

  def __init__(self, components, proportions):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # GMM
    self.components = components
    self.proportions = proportions
    self.d = self.components[0].d

  def cond(self, x):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Conditional GMM
    components = [c.cond(x) for c in self.components]
    return GMM(components, self.proportions)

  def sample(self, size=None):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """

    # Draw from a multinomial
    if size is None:
      nums = numpy.random.multinomial(1, self.proportions)
      c = nums.index(1) # which class got picked
      return self.components[c].sample()
    else:
      n = numpy.prod(size)
      if self.d == 1:
        out = numpy.empty((n,), dtype=float)
        nums = numpy.random.multinomial(n, self.proportions)
        i = 0
        for component, num in zip(self.components, nums):
          out[i:i+num] = component.sample(size=num)
          i += num
        out = out.reshape(size)
      else:
        out = numpy.empty((n, self.d), dtype=float)
        nums = numpy.random.multinomial(n, self.proportions)
        i = 0
        for component, num in zip(self.components, nums):
          out[i:i+num] = component.sample(size=num)
          i += num
        if isinstance(size, int):
          out = out.reshape((size, self.d))
        else:
          out = out.reshape(size+(self.d,))
      return out


###################################################################################################
# Prior Class
###################################################################################################

class Prior():
  """This class represents TODO.

  *Keyword arguments:*

    - argument1 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.

    - argument2 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.
  """

  def __init__(self, post=None, *args, **kwargs):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    if post is None:
      post = type(self)
    self._post = post

  def sample(self, size=None):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    raise NotImplementedError

  def like1(self, x, *args, **kwargs):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    raise NotImplementedError

  def likelihood(self, D, *args, **kwargs):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    return numpy.prod(self.like1(D, *args, **kwargs))

  def lnlikelihood(self, D, *args, **kwargs):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    return numpy.log(self.likelihood(D, *args, **kwargs))

  def __call__(self, *args):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    raise NotImplementedError

  def _post_params(self, D):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    raise NotImplementedError

  def post(self, D):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    return self._post(*self._post_params(D))

  def pred(self, x):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    raise NotImplementedError


###################################################################################################
# NormInvWish Class
###################################################################################################

class NormInvWish(Prior):
  """This class represents TODO.

  *Keyword arguments:*

    - argument1 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.

    - argument2 -- Short description. This argument represents a long description. It can be:
      - Possibility 1: A possibility 1.
      - Possibility 2: A possibility 2.
  """

  def __init__(self, mu_0, kappa_0, Lam_0, nu_0):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    self.mu_0 = numpy.array(mu_0, dtype=float)
    self.kappa_0 = float(kappa_0)
    self.Lam_0 = numpy.array(Lam_0, dtype=float)
    self.nu_0 = int(nu_0)
    self.d = len(mu_0)
    self.model_dtype = numpy.dtype([('mu', float, self.d), ('Sig', float, (self.d, self.d))])
    super(NormInvWish, self).__init__()

  def _S(self, D):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    Dbar = numpy.mean(D, axis=0)
    return numpy.dot((D-Dbar).T, (D-Dbar))

  def sample(self, size=None):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    Sig = random_invwish(dof=self.nu_0, invS=self.Lam_0, size=size)
    if size is None:
      ret = numpy.zeros(1, dtype=self.model_dtype)
      ret['Sig'] = Sig
      ret['mu'] = numpy.random.multivariate_normal(self.mu_0, Sig/self.kappa_0)
      return ret[0]
    else:
      ret = numpy.zeros(size, dtype=self.model_dtype)
      ret['Sig'] = Sig
      for r in ret.ravel():
        r['mu'] = numpy.random.multivariate_normal(self.mu_0, r['Sig']/self.kappa_0)
      return ret

  def like1(self, *args):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    if len(args) == 2:
      x, theta = args
      mu = theta['mu']
      Sig = theta['Sig']
    elif len(args) == 3:
      x, mu, Sig = args
    assert x.shape[-1] == self.d
    assert mu.shape[-1] == self.d
    assert Sig.shape[-1] == Sig.shape[-2] == self.d
    norm = numpy.sqrt((2*numpy.pi)**self.d * numpy.linalg.det(Sig))
    einsum = numpy.einsum("...i,...ij,...j", x-mu, numpy.linalg.inv(Sig), x-mu)
    return numpy.exp(-0.5*einsum)/norm

  def __call__(self, *args):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    if len(args) == 1:
      mu = args[0]['mu']
      Sig = args[0]['Sig']
    elif len(args) == 2:
      mu, Sig = args
    nu_0, d = self.nu_0, self.d
    Z = (2.0**(nu_0*d/2.0) * gammad(d, nu_0/2.0) * \
        (2.0*numpy.pi/self.kappa_0)**(d/2.0) / numpy.linalg.det(self.Lam_0)**(nu_0/2.0))
    detSig = numpy.linalg.det(Sig)
    invSig = numpy.linalg.inv(Sig)
    einsum = numpy.einsum("...i,...ij,...j", mu-self.mu_0, invSig, mu-self.mu_0)
    return 1./Z * detSig**(-((nu_0+d)/2.0+1.0)) * \
           numpy.exp(-0.5*numpy.trace(numpy.einsum("...ij,...jk->...ik", self.Lam_0, invSig), axis1=-2, axis2=-1) - self.kappa_0/2.0*einsum)

  def _post_params(self, D):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    shape = D.shape
    if len(shape) == 2:
      n = shape[0]
      Dbar = numpy.mean(D, axis=0)
    elif len(shape) == 1:
      n = 1
      Dbar = numpy.mean(D)
    kappa_n = self.kappa_0 + n
    nu_n = self.nu_0 + n
    mu_n = (self.kappa_0 * self.mu_0 + n * Dbar) / kappa_n
    x = (Dbar-self.mu_0)[:, numpy.newaxis]
    Lam_n = (self.Lam_0 + self._S(D) + self.kappa_0*n/kappa_n*numpy.dot(x, x.T))
    return mu_n, kappa_n, Lam_n, nu_n

  def pred(self, x):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    return multivariate_t_density(self.nu_0-self.d+1, self.mu_0, self.Lam_0*(self.kappa_0+1)/(self.kappa_0 - self.d + 1), x)

  def evidence(self, D):
    """Returns TODO.
    
    *Keyword arguments:*
    
      - argument -- An argument.
    
    *Return:*
    
      - return -- A return.
    """
    shape = D.shape
    if len(shape) == 2:
      n, d = shape
    elif len(shape) == 1:
      n, d = 1, shape[0]
    assert d == self.d
    mu_n, kappa_n, Lam_n, nu_n = self._post_params(D)
    detLam0 = numpy.linalg.det(self.Lam_0)
    detLamn = numpy.linalg.det(Lam_n)
    num = gammad(d, nu_n/2.0) * detLam0**(self.nu_0/2.0)
    den = numpy.pi**(n*d/2.0) * gammad(d, self.nu_0/2.0) * detLamn**(nu_n/2.0)
    return num/den * (self.kappa_0/kappa_n)**(d/2.0)

