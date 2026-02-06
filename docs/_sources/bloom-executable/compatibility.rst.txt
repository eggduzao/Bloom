.. _compatibility:


*******************************************
Working with Cooler, Juicer, and text files
*******************************************

bloom is fully compatible with Hi-C files from Cooler (``.cool`` and ``.mcool``) and Juicer (``.hic``).
There is no need to convert them to bloom format, you can use them directly in any ``bloom`` command.
Text files, such as HiC-Pro output or 4D Nucleome pairs files must be converted to bloom format
before they can be used in any commands


###############################
Cooler ``.cool`` and ``.mcool``
###############################


``.mcool`` files are multi-resolution, i.e. they contain matrices for not just
one, but multiple resolutions. Therefore there is a special ``@`` syntax for using these files,
which allow you to set the resolution which should be used for this analysis:

.. code::

   /path/to/cooler.mcool@<resolution>

For example, to load matrices at one megabase resolution

.. code::

   /path/to/cooler.mcool@1mb

Both human-readable resolutions such as ``100kb``, ``1mb``, etc, and integers like ``100000`` and ``1000000``
are supported. Note that the resolution of your choice must be available in the object, which is
generated outside of bloom.

.. note::

   Currently, the Cooler file format specification does not intend for expected values to be
   stored in the file itself. A lot of bloom functions depend on expected values, but because
   they are not available in Cooler files they are generated on the fly each time a command
   is run. bloom tries to be clever about this by caching expected values for a single command,
   but expect some slowdowns due to this for some computations. If this becomes an issue,
   we recommend converting to bloom format (``bloom from-cooler``) or to Juicer ``.hic``.


#####################
Juicer ``.hic`` files
#####################


``.hic`` files are multi-resolution, i.e. they contain matrices for not just
one, but multiple resolutions. Therefore there is a special ``@`` syntax for using these files,
which allow you to set the resolution which should be used for this analysis:

.. code::

   /path/to/juicer.hic@<resolution>

For example, to load matrices at one megabase resolution

.. code::

   /path/to/juicer.hic@1mb

Both human-readable resolutions such as ``100kb``, ``1mb``, etc, and integers like ``100000`` and ``1000000``
are supported. Note that the resolution of your choice must be available in the object, which is
generated outside of bloom.


~~~~~~~~~~~~~~~~~~~~~~~~
Choosing a normalisation
~~~~~~~~~~~~~~~~~~~~~~~~

Juicer files also support multiple normalisation methods. Currently these are ``VC`` (vanilla coverage),
``VC_SQRT`` (square root vanilla coverage), ``ICE`` (ICE matrix balancing), and ``KR`` (Knight-Ruiz matrix
balancing). You can choose between normalisation methods by adding another ``@<norm>`` to the file name
like this:

.. code::

   /path/to/juicer.hic@1mb@VC

Note that this only works for Juicer files, and is optional. If not specified, the KR norm will be used.


##########
Text files
##########

Text files from HiC-Pro or a similar format can be loaded with ``bloom from-txt`` (see :ref:`bloom_from_txt`).
4D nucleome files, which contain read pair entries, can be loaded with ``bloom pairs`` (see :ref:`bloom-pairs`).