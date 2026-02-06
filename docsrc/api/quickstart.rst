.. _quickstart:

=============================
Quickstart with the bloom API
=============================

After you have installed bloom (see :ref:`bloom_installation`), you can import the module
from a Python console or script:

.. code::

    import bloom

The following tutorials will assume that you have loaded the :code:`bloom` module in this
manner.

****************
Loading datasets
****************

Any analysis typically begins with loading datasets into your workspace. bloom tries to make this
as simple as possible with the :func:`~bloom.__init__.load` function.
If you already have processed Hi-C files, either from the :code:`bloom` command line
application (see :ref:`bloom-auto` or :ref:`bloom-modular`), or from a compatible Hi-C application
(:code:`.cool` or :code:`.mcool` from `Cooler <https://github.com/mirnylab/cooler>`_ or :code:`.hic` from
`Juicer <https://github.com/aidenlab/juicer>`_), simply load them into your workspace
using :func:`~bloom.__init__.load` - no need to specify the type of file you are loading:

.. code::

     data = bloom.load("/path/to/file.hic")

When dealing with multi-resolution Hi-C files such as :code:`.mcool` from Cooler or :code:`.hic` from
Juicer, you can load a specific resolution using the :code:`@` notation:

.. code::

     data = bloom.load("/path/to/file.mcool@25000")

:func:`~bloom.__init__.load` is not limited to Hi-C files, but also works on any other file
produced with bloom, such as :class:`~bloom.pairs.RegionPairs` files, :class:`~bloom.regions.Genome`,
analysis results like :class:`~bloom.architecture.comparisons.FoldChangeMatrix` and generally most
other bloom files.

:func:`~bloom.__init__.load` even works on most of the common file formats for genomic
datasets, such as BED, GFF, BigWig, Tabix, BEDPE and more. Try it out on your dataset of choice and
chances are :func:`~bloom.__init__.load` can handle it. And if it does not, consider raising
an issue on `Github <https://github.com/vaquerizaslab/bloom/issues>`_ to ask for support.

Internally, :func:`~bloom.__init__.load` finds a suitable class for the type of data
in the supplied file, and opens the file using that class. For example, the result of

.. code::

    hic = bloom.Hic("output/hic/binned/bloom_example_1mb.hic")

is equivalent to

.. code::

    hic = bloom.load("output/hic/binned/bloom_example_1mb.hic")

with the big advantage that you don't need to worry about remembering class names or
their location within the bloom module hierarchy. In both cases, the type of the
returned object is :code:`bloom.hic.Hic`:

.. code::

    # check the type fo the object
    type(hic)  # bloom.hic.Hic

Here are a few more examples:

.. code::

    cool = bloom.load("test.cool")
    type(cool)  # bloom.compatibility.cooler.CoolerHic

    juicer = bloom.load("test_juicer.hic")
    type(juicer)  # bloom.compatibility.juicer.JuicerHic

    fragments = bloom.load("hg19_chr18_19_re_fragments.bed")
    type(fragments)  # genomic_regions.regions.Bed

    bam = bloom.load("test.bam")
    type(bam)  # pysam.libcalignmentfile.AlignmentFile

    ins = bloom.load("architecture/domains/bloom_example_100kb.insulation")
    type(ins)  # bloom.architecture.domains.InsulationScores

    # and many other data types

The next section will discuss :ref:`common_interfaces` that make working with genomic data
in general and bloom objects specifically straightforward and simple.

*******
Logging
*******

bloom uses the ``logging`` module. In a ``python`` session, use a statement like

.. literalinclude:: generate/code/generate_example_code.py
    :language: python
    :start-after: start snippet logging
    :end-before: end snippet logging

to enable basic console logging. Have a look the
`logging documentation <https://docs.python.org/3/library/logging.html>`_
for more information on log levels and handlers.