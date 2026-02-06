.. _genomic_regions:

===========
RegionBased
===========

bloom builds extensively on the :code:`genomic_regions` package, which provides a unified
interface for most types of region-based genomic data. We highly recommend
`reading the documentation <https://vaquerizaslab.github.io/genomic_regions/>`_
of that package before going into the details of bloom, as many of the concepts discussed
therein are central to the handling of data in bloom.

You can check whether a bloom object supports the :class:`~genomic_regions.RegionBased`
interface with

.. code::

   import genomic_regions as gr
   isinstance(o, gr.RegionBased)  # True for objects supporting the regions interface

The current list of bloom objects supporting the :class:`~genomic_regions.RegionBased`
interface is:
:class:`~bloom.architecture.domains.InsulationScore`,
:class:`~bloom.architecture.domains.DirectionalityIndex`,
:class:`~bloom.architecture.domains.Boundaries`,
:class:`~bloom.architecture.domains.InsulationScores`,
:class:`~bloom.architecture.domains.DirectionalityIndexes`,
:class:`~bloom.architecture.comparisons.FoldChangeScores`,
:class:`~bloom.architecture.comparisons.DifferenceScores`,
:class:`~bloom.architecture.comparisons.DifferenceRegions`,
:class:`~bloom.architecture.comparisons.FoldChangeRegions`,
:class:`~bloom.compatibility.cooler.CoolerHic`,
:class:`~bloom.compatibility.juicer.JuicerHic`,
:class:`~bloom.hic.Hic`,
:class:`~bloom.architecture.compartments.ABCompartmentMatrix`,
:class:`~bloom.architecture.comparisons.DifferenceMatrix`,
:class:`~bloom.architecture.comparisons.FoldChangeMatrix`,
:class:`~bloom.peaks.PeakInfo`,
and
:class:`~bloom.peaks.RaoPeakInfo`.

Any object built on that foundation supports, for example, region iterators:

.. code::

   for region in hic.regions:
       print(region)
       print(region.chromosome, region.start, region.end, region.strand)
       print(region.is_forward)
       print(region.center)
       # ...

Range queries:

.. code::

   for region in hic.regions('chr1:3mb-12mb'):
       print(region.chromosome)  # chr1
       # ...

and many more convenient features. The object type returned by all of those queries
is :class:`~genomic_regions.GenomicRegion`, which has many convenient functions to
deal with region properties and operations.

.. code:: python

    len(region)  # returns the size of the region in base pairs
    region.center  # returns the base (or fraction of base) at the center of the region
    region.five_prime  # returns the starting base at the 5' end of the region
    region.three_prime  # returns the starting base at the 3' end of the region
    region.is_forward()  # True if strand is '+' or '+1'
    region.is_reverse()  # True if strand is '-' or '-1'
    region.attributes  # return all attribute names in this region object
    region.copy()  # return a shallow copy of this region
    region.to_string()  # return a region identifier string describing the region

    region = gr.as_region('chr12:12.5Mb-18Mb')
    region.overlaps('chr12:11Mb-13Mb')  # True
    region.overlaps('chr12:11Mb-11.5Mb')  # False
    region.overlaps('chr1:11Mb-13Mb')  # False

Refer to the
`genomic_regions documentation <https://github.com/vaquerizaslab/genomic_regions>`_ for
all the details.

Similarly to the :code:`regions` interface for handling collections of genomic regions,
bloom implements interfaces for working with pairs of genomic regions (:code:`edges`)
and matrix operations (:code:`matrix`). These work in exactly the same way for bloom,
Cooler, and Juicer files. Hence, all of these are directly compatible with bloom architectural
functions such as the insulation score or AB compartment analyses, ...

These interfaces will be introduced in the following sections, starting with :ref:`edges_interface`.