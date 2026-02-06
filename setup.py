import os
from setuptools import setup, find_packages, Command, Extension


__version__ = None
exec(open('bloom/version.py').read())


class CleanCommand(Command):
    """
    Custom clean command to tidy up the project root.
    """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info ./htmlcov')


setup(
    name='bloom',
    version=__version__,
    description='Framework for the ANalysis of C-data.',
    setup_requires=[
        'setuptools>=18.0',
        'cython'
    ],
    packages=find_packages(),
    package_data={'bloom': ['test/data/*/*']},
    include_package_data=True,
    install_requires=[
        'numpy>=1.16.0',
        'scipy',
        'pillow',
        'matplotlib>=3.1.0',
        'pandas>=0.15.0',
        'pysam>=0.9.1',
        'biopython',
        'pytest',
        'msgpack>=1.0.0',
        'msgpack-numpy>=0.4.6.1',
        'scikit-learn',
        'progressbar2',
        'pybedtools',
        'pyBigWig',
        'PyYAML>=5.1',
        'tables>=3.5.1',
        'seaborn',
        'future',
        'gridmap>=0.14.0',
        'intervaltree',
        'genomic_regions>=0.0.10',
        'scikit-image>=0.15.0',
        'cooler>=0.8.0',
        'h5py',
        'Deprecated',
    ],
    scripts=['bin/bloom', 'bin/bloomplot'],
    cmdclass={
        'clean': CleanCommand
    },
    ext_modules=[
        Extension(
            'bloom.tools.sambam',
            sources=['bloom/tools/sambam.pyx', 'bloom/tools/natural_cmp.c'],
        ),
    ],
)
