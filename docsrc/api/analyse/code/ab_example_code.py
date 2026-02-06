# start snippet ab setup
import bloom
import bloom.plotting as bloomplot
import matplotlib.pyplot as plt

hic_1mb = bloom.load("output/hic/binned/bloom_example_1mb.hic")
# end snippet ab setup

# start snippet alternative cooler
hic_1mb = bloom.load("architecture/other-hic/bloom_example.mcool@1mb")
# end snippet alternative cooler

# start snippet alternative juicer
hic_1mb = bloom.load("architecture/other-hic/bloom_example.juicer.hic@1mb")
# end snippet alternative juicer

# start snippet ab matrix
ab = bloom.ABCompartmentMatrix.from_hic(hic_1mb)
# end snippet ab matrix

# start snippet ab subset
ab_chr18 = ab.matrix(('chr18', 'chr18'))
# end snippet ab subset

# start snippet ab bloomplot-correlation
fig, ax = plt.subplots()
mp = bloomplot.SquareMatrixPlot(ab, ax=ax,
                           norm='lin', colormap='RdBu_r',
                           vmin=-1, vmax=1,
                           draw_minor_ticks=False)
mp.plot('chr18')
plt.show()
# end snippet ab bloomplot-correlation
fig.savefig('../docsrc/api/analyse/images/ab_1mb_correlation.png')


# start snippet ab ev
ev = ab.eigenvector()
# end snippet ab ev

# start snippet ab gc-ev
gc_ev = ab.eigenvector(genome='hg19_chr18_19.fa', force=True)
# end snippet ab gc-ev


# start snippet ab plot-ev
fig, ax = plt.subplots(figsize=(5, 2))
lp = bloomplot.LinePlot(ab, colors=['darkturquoise'])
lp.plot('chr18')
plt.show()
# end snippet ab plot-ev
fig.savefig('../docsrc/api/analyse/images/ab_1mb_ev.png')

# start snippet ab profile
profile, cutoffs = ab.enrichment_profile(hic_1mb, genome='hg19_chr18_19.fa')
# end snippet ab profile

# start snippet ab saddle
fig, axes = bloomplot.saddle_plot(profile, cutoffs)
# end snippet ab saddle
fig.savefig('../docsrc/api/analyse/images/ab_1mb_saddle.png')
