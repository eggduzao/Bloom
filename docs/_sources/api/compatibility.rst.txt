.. _api-compatibility:


************************************
Working with Cooler and Juicer files
************************************

bloom is fully compatible with Hi-C files from Cooler (``.cool`` and ``.mcool``) and Juicer (``.hic``).
There is no need to convert them to bloom format, you can use them directly.


###############################
Cooler ``.cool`` and ``.mcool``
###############################


``.mcool`` files are multi-resolution, i.e. they contain matrices for not just
one, but multiple resolutions. Therefore there is a special ``@`` syntax for using these files,
which allow you to set the resolution which should be used for this analysis:

.. code:: python

   hic = bloom.load("/path/to/cooler.mcool@<resolution>")

For example, to load matrices at one megabase resolution

.. code:: python

   hic = bloom.load("/path/to/cooler.mcool@1mb")

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

.. code:: python

   hic = bloom.load("/path/to/juicer.hic@<resolution>")

For example, to load matrices at one megabase resolution

.. code:: python

   hic = bloom.load("/path/to/juicer.hic@1mb")

Both human-readable resolutions such as ``100kb``, ``1mb``, etc, and integers like ``100000`` and ``1000000``
are supported. Note that the resolution of your choice must be available in the object, which is
generated outside of bloom.

Juicer files also support multiple normalisation methods. Currently these are ``VC`` (vanilla coverage),
``VC_SQRT`` (square root vanilla coverage), ``ICE`` (ICE matrix balancing), and ``KR`` (Knight-Ruiz matrix
balancing). You can choose between normalisation methods by adding another ``@<norm>`` to the file name
like this:

.. code::

   hic = bloom.load("/path/to/juicer.hic@1mb@VC")


Note that this only works for Juicer files, and is optional. If not specified, the KR norm will be used.
