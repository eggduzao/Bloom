import bloom
from bloom.data.registry import class_name_dict
from bloom.tools import dummy
import genomic_regions as gr
import pytest
import pysam
import os


class TestAuto:
    def test_auto_identification(self, tmpdir):
        for class_name in ('Hic', 'AccessOptimisedHic', 'FragmentMappedReadPairs', 'Reads', 'GenomicTrack',
                           'RaoPeakInfo', 'AccessOptimisedReadPairs'):
            file_name = str(tmpdir) + '/{}.h5'.format(class_name)
            cls_ = class_name_dict[class_name]
            x = cls_(file_name=file_name, mode='w')
            x.close()

            x = bloom.load(file_name, mode='r')
            assert isinstance(x, cls_)
            x.close()

    def test_hic_based_auto_identification(self, tmpdir):
        with dummy.sample_hic() as hic:
            for class_name in ('ABDomains', 'ABDomainMatrix', 'ExpectedContacts', 'ObservedExpectedRatio',
                               'PossibleContacts', 'RegionContactAverage',
                               'InsulationIndex', 'DirectionalityIndex'):
                file_name = str(tmpdir) + '/{}.h5'.format(class_name)
                cls_ = class_name_dict[class_name]
                x = cls_(hic, file_name=file_name, mode='w')
                x.close()

                x = bloom.load(file_name, mode='r')
                assert isinstance(x, cls_)
                x.close()
            for class_name in ('FoldChangeMatrix',):
                file_name = str(tmpdir) + '/{}.h5'.format(class_name)
                cls_ = class_name_dict[class_name]
                x = cls_(hic, hic, file_name=file_name, mode='w')
                x.close()

                x = bloom.load(file_name, mode='r')
                assert isinstance(x, cls_)
                x.close()

    def test_conversion(self, tmpdir):
        file_name = str(tmpdir) + '/x.hic'
        with dummy.sample_hic(file_name=file_name) as hic:
            # simulate old-style object
            hic.file.remove_node('/meta_information', recursive=True)

        hic = bloom.load(file_name, mode='r')
        assert isinstance(hic, bloom.Hic)
        hic.close()

        hic = bloom.Hic(file_name)
        hic.close()

        hic = bloom.load(file_name, mode='r')
        hic.close()
        assert isinstance(hic, bloom.Hic)

    def test_old_style_index(self, tmpdir):
        with dummy.sample_hic() as hic:
            for class_name in ('ABDomains', 'ABDomainMatrix', 'ExpectedContacts', 'ObservedExpectedRatio',
                               'ABDomains', 'PossibleContacts', 'RegionContactAverage',
                               'InsulationIndex', 'DirectionalityIndex'):
                file_name = str(tmpdir) + '/{}.h5'.format(class_name)
                cls_ = class_name_dict[class_name]
                x = cls_(hic, file_name=file_name, mode='w')
                # simulate missing meta-information
                x.close()

                x = bloom.load(file_name, mode='r')
                assert isinstance(x, cls_)
                x.close()

            for class_name in ('FoldChangeMatrix',):
                file_name = str(tmpdir) + '/{}.h5'.format(class_name)
                cls_ = class_name_dict[class_name]
                x = cls_(hic, hic, file_name=file_name, mode='w')
                # simulate missing meta-information
                x.close()

                x = bloom.load(file_name, mode='r')
                assert isinstance(x, cls_)
                x.close()

        for class_name in ('Hic', 'AccessOptimisedHic', 'FragmentMappedReadPairs', 'Reads', 'GenomicTrack'):
            file_name = str(tmpdir) + '/{}.h5'.format(class_name)
            cls_ = class_name_dict[class_name]
            x = cls_(file_name=file_name, mode='w')
            # simulate missing meta-information
            x.file.remove_node('/meta_information', recursive=True)
            x.close()

            x = bloom.load(file_name, mode='r')
            assert isinstance(x, cls_)
            x.close()

    def test_bed(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        bed_file = this_dir + '/test_auto/test.bed'

        with bloom.load(bed_file) as bed:
            assert isinstance(bed, gr.Bed)

        with pytest.raises(ValueError):
            foo_file = this_dir + '/test_auto/foo.txt'
            bloom.load(foo_file)

    def test_bigwig(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        bw_file = this_dir + '/test_auto/test.bw'

        with bloom.load(bw_file) as bw:
            assert isinstance(bw, gr.BigWig)

    def test_sambam(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        sam_file = this_dir + '/test_auto/test.sam'

        with bloom.load(sam_file, mode='r') as bw:
            assert isinstance(bw, pysam.AlignmentFile)

        bam_file = this_dir + '/test_auto/test.bam'

        with bloom.load(bam_file, mode='r') as bw:
            assert isinstance(bw, pysam.AlignmentFile)
