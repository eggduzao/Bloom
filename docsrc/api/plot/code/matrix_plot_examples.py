import os

# start snippet bloomplot import
import bloom
import bloom.plotting as bloomplot
# end snippet bloomplot import

# start snippet bloomplot matplotlib
import matplotlib.pyplot as plt
# end snippet bloomplot matplotlib

bloom_base = '..'
#bloom_base = '/Users/kkruse/dev/bloom'

# start snippet bloomplot load hic
hic = bloom.load("output/hic/binned/bloom_example_50kb.hic")
# end snippet bloomplot load hic

# start snippet bloomplot triangular string
hp = bloomplot.TriangularMatrixPlot(hic, vmax=0.05)
hp.plot('chr18:6mb-10mb')
hp.show()
# end snippet bloomplot triangular string

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_triangular.png'), figsize=(6, 3))


# start snippet bloomplot plt axes
fig, ax = plt.subplots()
hp = bloomplot.TriangularMatrixPlot(hic, vmax=0.05, ax=ax)
hp.plot('chr18:6mb-10mb')
ax.set_xticks([7500000, 8500000])
ax.set_xticklabels(['customise', 'everything!'])
hp.show()
# end snippet bloomplot plt axes

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_triangular_plt.png'), figsize=(6, 3))


# start snippet bloomplot square string
hp = bloomplot.SquareMatrixPlot(hic)
hp.plot('chr18:6mb-10mb')
hp.show()
# end snippet bloomplot square string

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_square.png'), figsize=(6, 6))


# start snippet bloomplot square vmax
hp = bloomplot.SquareMatrixPlot(hic, vmax=0.05)
hp.plot('chr18:6mb-10mb')
hp.show()
# end snippet bloomplot square vmax

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_square_vmax.png'), figsize=(6, 6))


# start snippet bloomplot square cmap
hp = bloomplot.SquareMatrixPlot(hic, vmax=0.05, colormap='white_red')
hp.plot('chr18:6mb-10mb')
hp.show()
# end snippet bloomplot square cmap

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_square_cmap.png'), figsize=(6, 6))


# start snippet bloomplot square log
hp = bloomplot.SquareMatrixPlot(hic, vmax=0.05, norm='log')
hp.plot('chr18:6mb-10mb')
hp.show()
# end snippet bloomplot square log

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_square_log.png'), figsize=(6, 6))

# start snippet bloomplot square uncorrected
hp = bloomplot.SquareMatrixPlot(hic, vmax=30, matrix_norm=False)
hp.plot('chr18:6mb-10mb')
hp.show()
# end snippet bloomplot square uncorrected

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_square_uncorrected.png'), figsize=(6, 6))


# start snippet bloomplot square oe
hp = bloomplot.SquareMatrixPlot(hic, vmin=-2, vmax=2, oe=True, log=True,
                               colormap='RdBu_r')
hp.plot('chr18:6mb-10mb')
hp.show()
# end snippet bloomplot square oe

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_square_oe.png'), figsize=(6, 6))


fig, ax = plt.subplots(figsize=(6, 3))
# start snippet bloomplot triangular maxdist
hp = bloomplot.TriangularMatrixPlot(hic, vmax=0.05, max_dist='2mb')
hp.plot('chr18:6mb-10mb')
hp.show()
# end snippet bloomplot triangular maxdist

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_triangular_maxdist.png'), figsize=(6, 3))


fig, ax = plt.subplots(figsize=(10, 10))
# start snippet bloomplot mirror
# first create two triangular plots
top_plot = bloomplot.TriangularMatrixPlot(hic, vmax=0.05, max_dist='2mb')
bottom_plot = bloomplot.TriangularMatrixPlot(hic, vmin=-2, vmax=2, oe=True, log=True, colormap='RdBu_r', max_dist='2mb')
# then merge them
hp = bloomplot.MirrorMatrixPlot(top_plot, bottom_plot)
hp.plot('chr18:6mb-10mb')
hp.show()
# end snippet bloomplot mirror

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_mirror.png'))