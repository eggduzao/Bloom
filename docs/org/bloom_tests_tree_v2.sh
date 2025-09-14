#!/bin/bash

mkdir -p /Users/egg/Projects/Bloom
mkdir -p /Users/egg/Projects/Bloom/tests
touch /Users/egg/Projects/Bloom/tests/conftest.py
mkdir -p /Users/egg/Projects/Bloom/tests/golden
mkdir -p /Users/egg/Projects/Bloom/tests/perf
mkdir -p /Users/egg/Projects/Bloom/tests/ui
mkdir -p /Users/egg/Projects/Bloom/tests/test_annotate
touch /Users/egg/Projects/Bloom/tests/test_annotate/test_ctcf.py
touch /Users/egg/Projects/Bloom/tests/test_annotate/test_chipseq.py
touch /Users/egg/Projects/Bloom/tests/test_annotate/test_enhancers.py
touch /Users/egg/Projects/Bloom/tests/test_annotate/test_lncrna.py
touch /Users/egg/Projects/Bloom/tests/test_annotate/test_repeats.py
touch /Users/egg/Projects/Bloom/tests/test_annotate/test_external_db.py
mkdir -p /Users/egg/Projects/Bloom/tests/test_cab
touch /Users/egg/Projects/Bloom/tests/test_cab/test_definitions.py
touch /Users/egg/Projects/Bloom/tests/test_cab/test_extraction.py
touch /Users/egg/Projects/Bloom/tests/test_cab/test_validation.py
touch /Users/egg/Projects/Bloom/tests/test_cab/test_visualization.py
mkdir -p /Users/egg/Projects/Bloom/tests/test_cab/test_models
mkdir -p /Users/egg/Projects/Bloom/tests/test_cli
touch /Users/egg/Projects/Bloom/tests/test_cli/test_main.py
touch /Users/egg/Projects/Bloom/tests/test_cli/test_parse.py
touch /Users/egg/Projects/Bloom/tests/test_cli/test_call_structures.py
touch /Users/egg/Projects/Bloom/tests/test_cli/test_annotate.py
touch /Users/egg/Projects/Bloom/tests/test_cli/test_metrics.py
touch /Users/egg/Projects/Bloom/tests/test_cli/test_model.py
touch /Users/egg/Projects/Bloom/tests/test_cli/test_visualize.py
mkdir -p /Users/egg/Projects/Bloom/tests/test_configs
touch /Users/egg/Projects/Bloom/tests/test_configs/test_base.py
mkdir -p /Users/egg/Projects/Bloom/tests/test_configs/test_data
mkdir -p /Users/egg/Projects/Bloom/tests/test_configs/test_deep_learning
mkdir -p /Users/egg/Projects/Bloom/tests/test_configs/test_rules
mkdir -p /Users/egg/Projects/Bloom/tests/test_configs/test_pipelines
mkdir -p /Users/egg/Projects/Bloom/tests/test_core
touch /Users/egg/Projects/Bloom/tests/test_core/test_base.py
touch /Users/egg/Projects/Bloom/tests/test_core/test_losses.py
touch /Users/egg/Projects/Bloom/tests/test_core/test_metrics.py
touch /Users/egg/Projects/Bloom/tests/test_core/test_schedulers.py
touch /Users/egg/Projects/Bloom/tests/test_core/test_logging.py
touch /Users/egg/Projects/Bloom/tests/test_core/test_enums.py
touch /Users/egg/Projects/Bloom/tests/test_core/test_paths.py
touch /Users/egg/Projects/Bloom/tests/test_core/test_config.py
touch /Users/egg/Projects/Bloom/tests/test_core/test_exceptions.py
touch /Users/egg/Projects/Bloom/tests/test_core/test_registry.py
touch /Users/egg/Projects/Bloom/tests/test_core/test_typing.py
mkdir -p /Users/egg/Projects/Bloom/tests/test_gui
touch /Users/egg/Projects/Bloom/tests/test_gui/test_app.py
touch /Users/egg/Projects/Bloom/tests/test_gui/test_loaders.py
touch /Users/egg/Projects/Bloom/tests/test_gui/test_layout.py
touch /Users/egg/Projects/Bloom/tests/test_gui/test_callbacks.py
mkdir -p /Users/egg/Projects/Bloom/tests/test_io
touch /Users/egg/Projects/Bloom/tests/test_io/test_hic_parser.py
touch /Users/egg/Projects/Bloom/tests/test_io/test_cool_parser.py
touch /Users/egg/Projects/Bloom/tests/test_io/test_anyc_parser.py
touch /Users/egg/Projects/Bloom/tests/test_io/test_bed_parser.py
touch /Users/egg/Projects/Bloom/tests/test_io/test_gtf_parser.py
touch /Users/egg/Projects/Bloom/tests/test_io/test_fasta_parser.py
touch /Users/egg/Projects/Bloom/tests/test_io/test_vcf_parser.py
touch /Users/egg/Projects/Bloom/tests/test_io/test_bam_parser.py
touch /Users/egg/Projects/Bloom/tests/test_io/test_crispr_parser.py
touch /Users/egg/Projects/Bloom/tests/test_io/test_lncrna_parser.py
touch /Users/egg/Projects/Bloom/tests/test_io/test_utils.py
mkdir -p /Users/egg/Projects/Bloom/tests/test_metrics
touch /Users/egg/Projects/Bloom/tests/test_metrics/test_reproducibility.py
touch /Users/egg/Projects/Bloom/tests/test_metrics/test_entropy.py
touch /Users/egg/Projects/Bloom/tests/test_metrics/test_similarity.py
touch /Users/egg/Projects/Bloom/tests/test_metrics/test_dynamic_score.py
touch /Users/egg/Projects/Bloom/tests/test_metrics/test_cab_finder.py
touch /Users/egg/Projects/Bloom/tests/test_metrics/test_statistical_tests.py
mkdir -p /Users/egg/Projects/Bloom/tests/test_models
touch /Users/egg/Projects/Bloom/tests/test_models/test_loop_predictor.py
touch /Users/egg/Projects/Bloom/tests/test_models/test_tad_predictor.py
touch /Users/egg/Projects/Bloom/tests/test_models/test_dynamics_model.py
touch /Users/egg/Projects/Bloom/tests/test_models/test_lncrna_model.py
touch /Users/egg/Projects/Bloom/tests/test_models/test_autoencoder.py
touch /Users/egg/Projects/Bloom/tests/test_models/test_interpretable.py
touch /Users/egg/Projects/Bloom/tests/test_models/test_utils.py
mkdir -p /Users/egg/Projects/Bloom/tests/test_structures
touch /Users/egg/Projects/Bloom/tests/test_structures/test_compartments.py
touch /Users/egg/Projects/Bloom/tests/test_structures/test_tads.py
touch /Users/egg/Projects/Bloom/tests/test_structures/test_loops.py
touch /Users/egg/Projects/Bloom/tests/test_structures/test_dynamics.py
touch /Users/egg/Projects/Bloom/tests/test_structures/test_phase_domains.py
touch /Users/egg/Projects/Bloom/tests/test_structures/test_multi_resolution.py
touch /Users/egg/Projects/Bloom/tests/test_structures/test_sc_structure.py
mkdir -p /Users/egg/Projects/Bloom/tests/test_utils
touch /Users/egg/Projects/Bloom/tests/test_utils/test_decorators.py
touch /Users/egg/Projects/Bloom/tests/test_utils/test_file_utils.py
touch /Users/egg/Projects/Bloom/tests/test_utils/test_settings.py
touch /Users/egg/Projects/Bloom/tests/test_utils/test_io_utils.py
touch /Users/egg/Projects/Bloom/tests/test_utils/test_seed.py
touch /Users/egg/Projects/Bloom/tests/test_utils/test_ops.py
touch /Users/egg/Projects/Bloom/tests/test_utils/test_config.py
touch /Users/egg/Projects/Bloom/tests/test_utils/test_timings.py
touch /Users/egg/Projects/Bloom/tests/test_utils/test_transforms.py
touch /Users/egg/Projects/Bloom/tests/test_utils/test_parallel.py
touch /Users/egg/Projects/Bloom/tests/test_utils/test_profiling.py
touch /Users/egg/Projects/Bloom/tests/test_utils/test_masks.py
touch /Users/egg/Projects/Bloom/tests/test_utils/test_metrics_helpers.py
touch /Users/egg/Projects/Bloom/tests/test_utils/test_schema.py
touch /Users/egg/Projects/Bloom/tests/test_utils/test_serialization.py
touch /Users/egg/Projects/Bloom/tests/test_utils/test_env.py
mkdir -p /Users/egg/Projects/Bloom/tests/test_viz
touch /Users/egg/Projects/Bloom/tests/test_viz/test_basic.py
touch /Users/egg/Projects/Bloom/tests/test_viz/test_density.py
touch /Users/egg/Projects/Bloom/tests/test_viz/test_heatmaps.py
touch /Users/egg/Projects/Bloom/tests/test_viz/test_confusion.py
touch /Users/egg/Projects/Bloom/tests/test_viz/test_pr_roc_curves.py
touch /Users/egg/Projects/Bloom/tests/test_viz/test_arcplot.py
touch /Users/egg/Projects/Bloom/tests/test_viz/test_dynamics_plot.py
touch /Users/egg/Projects/Bloom/tests/test_viz/test_genome_browser.py
touch /Users/egg/Projects/Bloom/tests/test_viz/test_tensorboard.py
touch /Users/egg/Projects/Bloom/tests/test_viz/test_grad_cam.py
touch /Users/egg/Projects/Bloom/tests/test_viz/test_meta_gene.py
touch /Users/egg/Projects/Bloom/tests/test_viz/test_umap_embedding.py
