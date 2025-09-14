
# Import
import os
import shutil
import subprocess

# Move legacy items
def move_items(mapping_dict, source_prefix, destination_prefix, flag_git=False):
    """
    Move files and directories according to mapping_dict, optionally using 'git mv'.

    Parameters:
        mapping_dict (dict): Keys are source paths relative to source_prefix;
                             values are destination paths relative to destination_prefix.
        source_prefix (str): Absolute or relative path prefix for source files.
        destination_prefix (str): Absolute or relative path prefix for destination.
        flag_git (bool): If True, use 'git mv' for moving.
    """

    for src_rel, dest_rel in mapping_dict.items():
        src_path = os.path.join(source_prefix, src_rel)
        dest_path = os.path.join(destination_prefix, dest_rel)

        # Ensure destination directory exists
        dest_dir = os.path.dirname(dest_path)
        os.makedirs(dest_dir, exist_ok=True)

        if flag_git:
            # Using git mv
            try:
                subprocess.check_call(['git', 'mv', src_path, dest_path])
                print(f"Moved with git: {src_path} -> {dest_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error using git mv: {e}")
        else:
            # Regular shutil.move
            try:
                shutil.move(src_path, dest_path)
                print(f"Moved: {src_path} -> {dest_path}")
            except shutil.Error as e:
                print(f"Error moving file: {e}")

##################### Main
if __name__ == "__main__":

    # Input
    src_prefix = "/Users/egg/Projects/Bloom"
    dst_prefix = "/Users/egg/Projects/Bloom/legacy"
    move_dict = {
        # bloom folder #---------------------------------------
        "bloom/barcode.py": "bloom/barcode.py",
        "bloom/contact_map.py": "bloom/contact_map.py",
        "bloom/core.py": "bloom/core.py",
        "bloom/dpmm.py": "bloom/dpmm.py",
        "bloom/goba.py": "bloom/goba.py",
        "bloom/ifs.py": "bloom/ifs.py",
        "bloom/io.py": "bloom/io.py",
        "bloom/io_bedgraph.py": "bloom/io_bedgraph.py",
        "bloom/io_cooler.py": "bloom/io_cooler.py",
        "bloom/io_juicer.py": "bloom/io_juicer.py",
        "bloom/preprocess.py": "bloom/preprocess.py",
        "bloom/sica.py": "bloom/sica.py",
        "bloom/util.py": "bloom/util.py",
        "bloom/visualization.py": "bloom/visualization.py",
        # c folder #-------------------------------------------
        "c/add_gaussian.c": "c/add_gaussian.c",
        "c/alpha_cut.c": "c/alpha_cut.c",
        "c/alpha_utils.c": "c/alpha_utils.c",
        "c/auto_linear.c": "c/auto_linear.c",
        "c/auto_non_linear.c": "c/auto_non_linear.c",
        "c/chol_update.cpp": "c/chol_update.cpp",
        "c/component.cpp": "c/component.cpp",
        "c/derive_from.c": "c/derive_from.c",
        "c/derive_to.c": "c/derive_to.c",
        "c/dirichlet.c": "c/dirichlet.c",
        "c/dirichlet_mix.c": "c/dirichlet_mix.c",
        "c/dirichlet_mix_em.c": "c/dirichlet_mix_em.c",
        "c/dual_binom.c": "c/dual_binom.c",
        "c/dual_gamma.c": "c/dual_gamma.c",
        "c/factorial_large_number.c": "c/factorial_large_number.c",
        "c/flops.c": "c/flops.c",
        "c/gamma_ln.c": "c/gamma_ln.c",
        "c/gauss_elimination.c": "c/gauss_elimination.c",
        "c/helpers.cpp": "c/helpers.cpp",
        "c/interpolation.c": "c/interpolation.c",
        "c/matricial_forms.c": "c/matricial_forms.c",
        "c/mixture.cpp": "c/mixture.cpp",
        "c/modules.cpp": "c/modules.cpp",
        "c/multi_gamma.c": "c/multi_gamma.c",
        "c/nd_sum.c": "c/nd_sum.c",
        "c/negative_binom.c": "c/negative_binom.c",
        "c/ode_forward_euler.c": "c/ode_forward_euler.c",
        "c/ode_midpoint_euler.c": "c/ode_midpoint_euler.c",
        "c/ode_semi_implicit_euler.c": "c/ode_semi_implicit_euler.c",
        "c/overcome_integer.c": "c/overcome_integer.c",
        "c/qr_eigen_values.c": "c/qr_eigen_values.c",
        "c/quaternions.c": "c/quaternions.c",
        "c/registry.c": "c/registry.c",
        "c/rep_mat.c": "c/rep_mat.c",
        "c/solve_dirichlet.c": "c/solve_dirichlet.c",
        "c/solve_mixture.c": "c/solve_mixture.c",
        "c/strong_number.c": "c/strong_number.c",
        "c/table.c": "c/table.c",
        "c/tetra_gamma.c": "c/tetra_gamma.c",
        "c/timing.cpp": "c/timing.cpp",
        "c/tri_gamma.c": "c/tri_gamma.c",
        "c/util.c": "c/util.c",
        "c/vectors_3d.c": "c/vectors_3d.c",
        "c/wishart.cpp": "c/wishart.cpp",
        "c/zero_prob.c": "c/zero_prob.c",
        # data folder #----------------------------------------
        "data/bin/juicer_tools_1.22.01.jar": "data/bin/juicer_tools_1.22.01.jar",
        "data/chrom_sizes/chrom.sizes.hg19": "data/chrom_sizes/chrom.sizes.hg19",
        "data/chrom_sizes/chrom.sizes.hg38": "data/chrom_sizes/chrom.sizes.hg38",
        "data/chrom_sizes/chrom.sizes.mm10": "data/chrom_sizes/chrom.sizes.mm10",
        "data/chrom_sizes/chrom.sizes.mm9": "data/chrom_sizes/chrom.sizes.mm9",
        "data/chrom_sizes/chrom.sizes.zv10": "data/chrom_sizes/chrom.sizes.zv10",
        "data/chrom_sizes/chrom.sizes.zv9": "data/chrom_sizes/chrom.sizes.zv9",
        "data/data.config": "data/data.config",
        "data/exclist/hg19.bed": "data/exclist/hg19.bed",
        "data/exclist/hg38_minimal.bed": "data/exclist/hg38_minimal.bed",
        "data/exclist/mm10.bed": "data/exclist/mm10.bed",
        "data/exclist/mm10_2.bed": "data/exclist/mm10_2.bed",
        "data/exclist/mm10_minimal.bed": "data/exclist/mm10_minimal.bed",
        "data/exclist/mm10_minimal_2.bed": "data/exclist/mm10_minimal_2.bed",
        "data/exclist/mm9.bed": "data/exclist/mm9.bed",
        "data/exclist/zv10.bed": "data/exclist/zv10.bed",
        "data/exclist/zv9.bed": "data/exclist/zv9.bed",
        "data/setup_environment.py": "data/setup_environment.py",
        # test folder #----------------------------------------
        "test/bg_to_hic.py": "test/bg_to_hic.py",
        "test/hic_to_bg.py": "test/hic_to_bg.py",
        "test/install.sh": "test/install.sh",
        "test/sparsity.py": "test/sparsity.py",
        "test/standard_test/bg_to_hic.py": "test/standard_test/bg_to_hic.py",
        "test/standard_test/commands.sh": "test/standard_test/commands.sh",
        "test/standard_test/input/MESC_25000_chr14_10Mtest.bg": "test/standard_test/input/MESC_25000_chr14_10Mtest.bg",
        "test/standard_test/output_to_check/output_contacts.bg": "test/standard_test/output_to_check/output_contacts.bg",
        "test/standard_test/output_to_check/output_matrix.bg": "test/standard_test/output_to_check/output_matrix.bg",
        "test/standard_test/output_to_check/output_matrix.bg.hic": "test/standard_test/output_to_check/output_matrix.bg.hic",
        "test/test_10_pipeline.py": "test/test_10_pipeline.py",
        "test/test_10_pipeline.sh": "test/test_10_pipeline.sh",
        "test/test_1_contact_map.py": "test/test_1_contact_map.py",
        "test/test_2_util.py": "test/test_2_util.py",
        "test/test_3_io_bedgraph.py": "test/test_3_io_bedgraph.py",
        "test/test_4_io_juicer.py": "test/test_4_io_juicer.py",
        "test/test_5_io_cooler.py": "test/test_5_io_cooler.py",
        "test/test_6_io.py": "test/test_6_io.py",
        "test/test_7_barcode.py": "test/test_7_barcode.py",
        "test/test_8_pipeline.py": "test/test_8_pipeline.py",
        "test/test_9_pipeline.sh": "test/test_9_pipeline.sh"
    }

    move_items(move_dict, source_prefix=src_prefix, destination_prefix=dst_prefix, flag_git=True)

