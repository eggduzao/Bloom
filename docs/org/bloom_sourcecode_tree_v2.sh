#!/bin/bash

mkdir -p /Users/egg/Projects/Bloom
mkdir -p /Users/egg/Projects/Bloom/src
mkdir -p /Users/egg/Projects/Bloom/src/bloom
touch /Users/egg/Projects/Bloom/src/bloom/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/__main__.py
touch /Users/egg/Projects/Bloom/src/bloom/__about__.py
touch /Users/egg/Projects/Bloom/src/bloom/_version.py
touch /Users/egg/Projects/Bloom/src/bloom/_typing.py
touch /Users/egg/Projects/Bloom/src/bloom/_registry.py
touch /Users/egg/Projects/Bloom/src/bloom/_compat.py
touch /Users/egg/Projects/Bloom/src/bloom/_typing.py
touch /Users/egg/Projects/Bloom/src/bloom/_registry.py
touch /Users/egg/Projects/Bloom/src/bloom/settings.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/annotate
touch /Users/egg/Projects/Bloom/src/bloom/annotate/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/annotate/ctcf.py
touch /Users/egg/Projects/Bloom/src/bloom/annotate/chipseq.py
touch /Users/egg/Projects/Bloom/src/bloom/annotate/enhancers.py
touch /Users/egg/Projects/Bloom/src/bloom/annotate/lncrna.py
touch /Users/egg/Projects/Bloom/src/bloom/annotate/repeats.py
touch /Users/egg/Projects/Bloom/src/bloom/annotate/external_db.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/cab
touch /Users/egg/Projects/Bloom/src/bloom/cab/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/cab/definitions.py
touch /Users/egg/Projects/Bloom/src/bloom/cab/extraction.py
touch /Users/egg/Projects/Bloom/src/bloom/cab/validation.py
touch /Users/egg/Projects/Bloom/src/bloom/cab/visualization.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/cab/models
touch /Users/egg/Projects/Bloom/src/bloom/cab/models/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/cab/models/main.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/cab/models/preprocessing
touch /Users/egg/Projects/Bloom/src/bloom/cab/models/preprocessing/__init__.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/cab/models/imputation
touch /Users/egg/Projects/Bloom/src/bloom/cab/models/imputation/__init__.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/cab/models/normalization
touch /Users/egg/Projects/Bloom/src/bloom/cab/models/normalization/__init__.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/cab/models/nn
touch /Users/egg/Projects/Bloom/src/bloom/cab/models/nn/__init__.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/cab/models/heads
touch /Users/egg/Projects/Bloom/src/bloom/cab/models/heads/__init__.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/cab/models/losses
touch /Users/egg/Projects/Bloom/src/bloom/cab/models/losses/__init__.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/cab/models/metrics
touch /Users/egg/Projects/Bloom/src/bloom/cab/models/metrics/__init__.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/cab/models/engine
touch /Users/egg/Projects/Bloom/src/bloom/cab/models/engine/__init__.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/cab/models/inference
touch /Users/egg/Projects/Bloom/src/bloom/cab/models/inference/__init__.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/cab/models/backends
touch /Users/egg/Projects/Bloom/src/bloom/cab/models/backends/__init__.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/cli
touch /Users/egg/Projects/Bloom/src/bloom/cli/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/cli/main.py
touch /Users/egg/Projects/Bloom/src/bloom/cli/parse.py
touch /Users/egg/Projects/Bloom/src/bloom/cli/call_structures.py
touch /Users/egg/Projects/Bloom/src/bloom/cli/annotate.py
touch /Users/egg/Projects/Bloom/src/bloom/cli/metrics.py
touch /Users/egg/Projects/Bloom/src/bloom/cli/model.py
touch /Users/egg/Projects/Bloom/src/bloom/cli/visualize.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/configs
touch /Users/egg/Projects/Bloom/src/bloom/configs/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/configs/base.yaml
mkdir -p /Users/egg/Projects/Bloom/src/bloom/configs/data
touch /Users/egg/Projects/Bloom/src/bloom/configs/data/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/configs/data/sequence_formats.json
touch /Users/egg/Projects/Bloom/src/bloom/configs/data/variant_formats.json
touch /Users/egg/Projects/Bloom/src/bloom/configs/data/genome_formats.json
touch /Users/egg/Projects/Bloom/src/bloom/configs/data/alignment_formats.json
touch /Users/egg/Projects/Bloom/src/bloom/configs/data/ucsc_formats.json
touch /Users/egg/Projects/Bloom/src/bloom/configs/data/lncrna_formats.json
touch /Users/egg/Projects/Bloom/src/bloom/configs/data/crispr_formats.json
touch /Users/egg/Projects/Bloom/src/bloom/configs/data/hic_formats.json
touch /Users/egg/Projects/Bloom/src/bloom/configs/data/tabular_formats.json
touch /Users/egg/Projects/Bloom/src/bloom/configs/data/preprocessing.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/data/postprocessing.yaml
mkdir -p /Users/egg/Projects/Bloom/src/bloom/configs/deep_learning
touch /Users/egg/Projects/Bloom/src/bloom/configs/deep_learning/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/configs/deep_learning/cab_base.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/deep_learning/cab_schedules.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/deep_learning/cab_optimizer.yaml
mkdir -p /Users/egg/Projects/Bloom/src/bloom/configs/deep_learning/train
mkdir -p /Users/egg/Projects/Bloom/src/bloom/configs/deep_learning/test
mkdir -p /Users/egg/Projects/Bloom/src/bloom/configs/deep_learning/model
mkdir -p /Users/egg/Projects/Bloom/src/bloom/configs/rules
touch /Users/egg/Projects/Bloom/src/bloom/configs/rules/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/configs/rules/optimizer.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/rules/schedules.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/rules/genome.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/rules/wgs_wes.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/rules/chipseq.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/rules/rnaseq.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/rules/atacseq.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/rules/lncrna.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/rules/crispr.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/rules/hic.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/rules/cab.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/rules/callbacks.yaml
mkdir -p /Users/egg/Projects/Bloom/src/bloom/configs/pipelines
touch /Users/egg/Projects/Bloom/src/bloom/configs/pipelines/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/configs/pipelines/full_bloom.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/pipelines/hic_processing.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/pipelines/lnc_processing.yaml
touch /Users/egg/Projects/Bloom/src/bloom/configs/pipelines/crispr_processing.yaml
mkdir -p /Users/egg/Projects/Bloom/src/bloom/core
touch /Users/egg/Projects/Bloom/src/bloom/core/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/core/base.py
touch /Users/egg/Projects/Bloom/src/bloom/core/losses.py
touch /Users/egg/Projects/Bloom/src/bloom/core/metrics.py
touch /Users/egg/Projects/Bloom/src/bloom/core/schedulers.py
touch /Users/egg/Projects/Bloom/src/bloom/core/logging.py
touch /Users/egg/Projects/Bloom/src/bloom/core/enums.py
touch /Users/egg/Projects/Bloom/src/bloom/core/paths.py
touch /Users/egg/Projects/Bloom/src/bloom/core/config.py
touch /Users/egg/Projects/Bloom/src/bloom/core/exceptions.py
touch /Users/egg/Projects/Bloom/src/bloom/core/_registry.py
touch /Users/egg/Projects/Bloom/src/bloom/core/_typing.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/gui
touch /Users/egg/Projects/Bloom/src/bloom/gui/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/gui/app.py
touch /Users/egg/Projects/Bloom/src/bloom/gui/loaders.py
touch /Users/egg/Projects/Bloom/src/bloom/gui/layout.py
touch /Users/egg/Projects/Bloom/src/bloom/gui/callbacks.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/io
touch /Users/egg/Projects/Bloom/src/bloom/io/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/io/hic_parser.py
touch /Users/egg/Projects/Bloom/src/bloom/io/cool_parser.py
touch /Users/egg/Projects/Bloom/src/bloom/io/anyc_parser.py
touch /Users/egg/Projects/Bloom/src/bloom/io/bed_parser.py
touch /Users/egg/Projects/Bloom/src/bloom/io/gtf_parser.py
touch /Users/egg/Projects/Bloom/src/bloom/io/fasta_parser.py
touch /Users/egg/Projects/Bloom/src/bloom/io/vcf_parser.py
touch /Users/egg/Projects/Bloom/src/bloom/io/bam_parser.py
touch /Users/egg/Projects/Bloom/src/bloom/io/crispr_parser.py
touch /Users/egg/Projects/Bloom/src/bloom/io/lncrna_parser.py
touch /Users/egg/Projects/Bloom/src/bloom/io/utils.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/metrics
touch /Users/egg/Projects/Bloom/src/bloom/metrics/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/metrics/reproducibility.py
touch /Users/egg/Projects/Bloom/src/bloom/metrics/entropy.py
touch /Users/egg/Projects/Bloom/src/bloom/metrics/similarity.py
touch /Users/egg/Projects/Bloom/src/bloom/metrics/dynamic_score.py
touch /Users/egg/Projects/Bloom/src/bloom/metrics/cab_finder.py
touch /Users/egg/Projects/Bloom/src/bloom/metrics/statistical_tests.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/models
touch /Users/egg/Projects/Bloom/src/bloom/models/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/models/loop_predictor.py
touch /Users/egg/Projects/Bloom/src/bloom/models/tad_predictor.py
touch /Users/egg/Projects/Bloom/src/bloom/models/dynamics_model.py
touch /Users/egg/Projects/Bloom/src/bloom/models/lncrna_model.py
touch /Users/egg/Projects/Bloom/src/bloom/models/autoencoder.py
touch /Users/egg/Projects/Bloom/src/bloom/models/interpretable.py
touch /Users/egg/Projects/Bloom/src/bloom/models/utils.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/structures
touch /Users/egg/Projects/Bloom/src/bloom/structures/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/structures/compartments.py
touch /Users/egg/Projects/Bloom/src/bloom/structures/tads.py
touch /Users/egg/Projects/Bloom/src/bloom/structures/loops.py
touch /Users/egg/Projects/Bloom/src/bloom/structures/dynamics.py
touch /Users/egg/Projects/Bloom/src/bloom/structures/phase_domains.py
touch /Users/egg/Projects/Bloom/src/bloom/structures/multi_resolution.py
touch /Users/egg/Projects/Bloom/src/bloom/structures/sc_structure.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/utils
touch /Users/egg/Projects/Bloom/src/bloom/utils/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/utils/decorators.py
touch /Users/egg/Projects/Bloom/src/bloom/utils/file_utils.py
touch /Users/egg/Projects/Bloom/src/bloom/utils/settings.py
touch /Users/egg/Projects/Bloom/src/bloom/utils/io_utils.py
touch /Users/egg/Projects/Bloom/src/bloom/utils/seed.py
touch /Users/egg/Projects/Bloom/src/bloom/utils/ops.py
touch /Users/egg/Projects/Bloom/src/bloom/utils/config.py
touch /Users/egg/Projects/Bloom/src/bloom/utils/timings.py
touch /Users/egg/Projects/Bloom/src/bloom/utils/transforms.py
touch /Users/egg/Projects/Bloom/src/bloom/utils/parallel.py
touch /Users/egg/Projects/Bloom/src/bloom/utils/profiling.py
touch /Users/egg/Projects/Bloom/src/bloom/utils/masks.py
touch /Users/egg/Projects/Bloom/src/bloom/utils/metrics_helpers.py
touch /Users/egg/Projects/Bloom/src/bloom/utils/schema.py
touch /Users/egg/Projects/Bloom/src/bloom/utils/serialization.py
touch /Users/egg/Projects/Bloom/src/bloom/utils/env.py
mkdir -p /Users/egg/Projects/Bloom/src/bloom/viz
touch /Users/egg/Projects/Bloom/src/bloom/viz/__init__.py
touch /Users/egg/Projects/Bloom/src/bloom/viz/basic.py
touch /Users/egg/Projects/Bloom/src/bloom/viz/density.py
touch /Users/egg/Projects/Bloom/src/bloom/viz/heatmaps.py
touch /Users/egg/Projects/Bloom/src/bloom/viz/confusion.py
touch /Users/egg/Projects/Bloom/src/bloom/viz/pr_roc_curves.py
touch /Users/egg/Projects/Bloom/src/bloom/viz/arcplot.py
touch /Users/egg/Projects/Bloom/src/bloom/viz/dynamics_plot.py
touch /Users/egg/Projects/Bloom/src/bloom/viz/genome_browser.py
touch /Users/egg/Projects/Bloom/src/bloom/viz/tensorboard.py
touch /Users/egg/Projects/Bloom/src/bloom/viz/grad_cam.py
touch /Users/egg/Projects/Bloom/src/bloom/viz/meta_gene.py
touch /Users/egg/Projects/Bloom/src/bloom/viz/umap_embedding.py
