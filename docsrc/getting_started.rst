###############
Getting started
###############

.. contents::
   :depth: 2

********
Overview
********

bloom is a Python (3.6+) toolkit for the analysis and visualisation of Hi-C data.
For common tasks, you can use the ``bloom`` executable. For more advanced analyses, bloom
can be imported as a powerful Python module.

Beyond objects generated within bloom, the toolkit is largely compatible with Hi-C files from
`Cooler <https://github.com/mirnylab/cooler>`_ and `Juicer <https://github.com/aidenlab/juicer>`_.


.. _bloom_installation:

************
Installation
************

Before installing bloom, make sure you have all the prerequisites installed on your system.
Specifically, bloom uses the HDF5 file format internally (via PyTables) to handle the large
amount of data typically generated in Hi-C experiments. The minimum required version of HDF5
is 1.8.4, which may already be installed on your machine.

.. note::

    It is generally not necessary to install HDF5 manually, as some version will typically be
    installed on any current Unix system, including macOS. If you can install bloom via pip
    (see below) and ``bloom --version`` returns a version number, you are most likely good to go.

Prerequisite: HDF5
==================

If you are on Linux, download the source code of the latest version from
the `HDF5 website <https://www.hdfgroup.org/HDF5/>`_ and unpack it.

.. code:: bash

   # make a new directory
   mkdir hdf5-build
   cd hdf5-build
   # replace xx with current version number
   wget https://support.hdfgroup.org/ftp/HDF5/current/src/hdf5-1.8.xx.tar.gz
   # unpack
   tar xzf hdf5-1.8.xx.tar.gz
   cd hdf5-1.8.xx/
   # use --prefix to set the folder in which HDF5 should be installed
   # alternatively, you can omit --prefix=... here and run
   # sudo make install to install globally (requires admin rights)
   ./configure --prefix=/path/to/hdf5/dir
   make
   make install

If you are on OS X or macOS, we highly recommend using the fantastic `Homebrew <http://brew.sh/>`_.
Then you can simply:

.. code:: bash

   brew install hdf5@1.8

To ensure that PyTables, the Python library that uses HDF5, finds the correct HDF5 version, we
need to set an environment variable pointing to the installation directory:

.. code:: bash

   # on Linux, this is the same /path/to/hdf5/dir that you used above
   # on macOS, this is wherever brew installs its recipies (typically /usr/local/Cellar)
   #   - you can find this by running 'brew info hdf5'
   export HDF5_DIR=/path/to/hdf5/dir


=====
bloom
=====

We strongly recommend installing bloom in a fresh virtual environment to prevent dependency 
issues. You can do this with tools like `pyenv <https://github.com/pyenv/pyenv>`_ or manually 
using `venv`, for example:

.. code:: bash

   # create local virtual environment in current folder
   python -m venv ./venv
   # activate virtual environment
   source venv/bin/activate

The simplest way to install bloom is via pip:

.. code:: bash

   pip install bloom

and that should be all you need! If you are not the owner of the Python installation,
try:

.. code:: bash

   pip install --user bloom

In some cases when using a virtual environment executables aren't in the proper ``PATH``,
then you can use

.. code:: bash

   python -m pip install bloom

You can also directly download the bloom source code from Github by cloning its repository.
The installation is then done via setup.py:

.. code:: bash

   git clone http://www.github.com/vaquerizaslab/bloom
   cd bloom
   pip install .

bloom can now be accessed via command line (``bloom`` for analysis, ``bloomplot`` for plotting)
or as a Python 3.6+ module (``import bloom``).

.. _dev_version:

~~~~~~~~~~~
Dev version
~~~~~~~~~~~

If you want the latest improvements, and can live with a higher likelihood of unresolved issues,
you can become a beta tester and check out the ``dev`` channel! We would appreciate feedback on
GitHub for any issue that you encounter.

.. code:: bash

   git clone http://www.github.com/vaquerizaslab/bloom
   git checkout dev
   cd bloom
   pip install -e .


.. warning::

    On some systems the installation of bloom using the above method will fail with a Cython
    dependency error. In this case, installing Cython and pysam prior to bloom might solve the issue:

    .. code:: bash

        pip uninstall bloom
        pip uninstall pysam
        pip install Cython
        pip install pysam
        pip install bloom

    If you are still experiencing problems during the installation, please raise an
    `issue on GitHub <https://github.com/vaquerizaslab/bloom/issues>`_.


~~~~~~~~
Bioconda
~~~~~~~~

.. _conda_note:

.. warning::

    We no longer support installations via ``conda`` due to a large amount of dependency 
    issues - please use a fresh virtual Python environment as detailed above!

    An older bloom package is also available via `Bioconda <https://bioconda.github.io/>`_, 
    but due to an unresolved dependency issue it is currently limited to Python 3.7.X and will not be 
    updated. Please refer to the
    `pull request thread <https://github.com/bioconda/bioconda-recipes/pull/23911>`_ for additional
    details.

    We strongly recommend installing bloom via ``pip`` - only then you will obtain the latest bug fixes 
    and features!


***************************
Building this documentation
***************************

If you want to build this documentation on your local machine, first make sure to install the
prerequisites by running

.. code:: bash

   pip install sphinx sphinx_rtd_theme sphinx-argparse

Then navigate to the :code:`docsrc` folder (assuming you are in the :code:`bloom` base folder):

.. code:: bash

   cd docsrc

Type :code:`make` to get a list of possible documentation outputs, for HTML use:

.. code:: bash

   make html

You will find the html output in :code:`_build/html`.


.. _example-bloom-auto:

****************
Example analysis
****************

For this example, we are going to use the command ``bloom auto`` (see :ref:`bloom-auto`) to
construct a Hi-C map from a subset of a previously published adrenal tissue data set
(`SRR4271982 of GSM2322539 <https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM2322539>`_).

You can download the files from `our Keeper library <https://keeper.mpdl.mpg.de/d/147906745b634c779ed3/>`_:

.. code:: bash

   wget -O examples.zip "https://keeper.mpdl.mpg.de/d/147906745b634c779ed3/files/?p=/examples.zip&dl=1"
   unzip examples.zip
   cd examples

From the examples folder, run:

.. code:: bash

   bloom auto SRR4271982_chr18_19_1.fastq.gzip SRR4271982_chr18_19_2.fastq.gzip output/ \
             -g hg19_chr18_19.fa -i hg19_chr18_19/hg19_chr18_19 -n bloom_example -t 4 -r HindIII \
             --split-ligation-junction -q 30 --run-with test

The ``--run-with test`` argument causes ``bloom`` to only print the commands it would execute, but
to exit before running any processing steps. Use this to review the pipeline and ensure you chose
the right parameters and that there are no errors.

When you remove the ``--run-with test`` argument, ``bloom`` will work through the pipeline.
On a modern desktop computer with at least four computing cores the command should take less
than 30 minutes to finish. It will generate several binned, bias-corrected Hi-C matrices from the
FASTQ input.

You can read details about ``bloom auto`` and all of its parameters in :ref:`bloom-auto`.


Plotting
========

We can plot the newly generated Hi-C maps easily using the ``bloomplot`` command. Simply execute

.. code:: bash

   bloomplot chr18:63mb-70mb -p triangular -vmax 0.05 output/hic/binned/bloom_example_100kb.hic

This will plot the region 63-70Mb of chromosome 18 in the familiar Hi-C plot.
Note that this dataset is very small and hence the quality of the matrix not
particularly great - but TADs are clearly visible.

.. image:: bloom-executable/bloom-generate-hic/images/chr18_63-70Mb.png

You can find details about the plotting executable ``bloomplot`` in :ref:`bloomplot-executable`.

Next steps
==========

Find out more about ``bloom auto`` and its parameters in :ref:`bloom-auto`. If you are interested
in customising individual steps of the pipeline, or in exploring all of bloom's analysis options,
have a look at :ref:`bloom-modular`. For more plotting functions, continue to :ref:`bloomplot-executable`.
To access bloom functionality from within Python, check out :ref:`bloom-api`.
