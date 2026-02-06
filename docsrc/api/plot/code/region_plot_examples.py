import os
import bloom
import bloom.plotting as bloomplot

# start snippet bloomplot matplotlib
import matplotlib.pyplot as plt
# end snippet bloomplot matplotlib

#bloom_base = '..'
bloom_base = '/Users/kkruse/dev/bloom'

# start snippet bloomplot load bed
insulation_scores_1mb = bloom.load("architecture/domains/bloom_example_100kb.insulation_1mb.bed")
insulation_scores_2mb = bloom.load("architecture/domains/bloom_example_100kb.insulation_2mb.bed")
boundaries_1mb = bloom.load("architecture/domains/bloom_example_100kb.insulation_boundaries_1mb.bed")
boundaries_2mb = bloom.load("architecture/domains/bloom_example_100kb.insulation_boundaries_2mb.bed")
# end snippet bloomplot load bed

# start snippet bloomplot line fill
hp = bloomplot.LinePlot(insulation_scores_1mb)
hp.plot('chr18:6mb-10mb')
hp.show()
# end snippet bloomplot line fill

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_line.png'))

# start snippet bloomplot line nofill
hp = bloomplot.LinePlot(insulation_scores_1mb, fill=False)
hp.plot('chr18:6mb-10mb')
hp.show()
# end snippet bloomplot line nofill

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_line_nofill.png'))

# start snippet bloomplot line mid
hp = bloomplot.LinePlot(insulation_scores_1mb, style='mid')
hp.plot('chr18:6mb-10mb')
hp.show()
# end snippet bloomplot line mid

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_line_mid.png'))

# start snippet bloomplot line col
hp = bloomplot.LinePlot(insulation_scores_1mb, style='mid', colors='cyan',
                       plot_kwargs={'alpha': 0.5})
hp.plot('chr18:6mb-10mb')
hp.show()
# end snippet bloomplot line col

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_line_col.png'))

# start snippet bloomplot line ylim
hp = bloomplot.LinePlot(insulation_scores_1mb, style='mid', colors='cyan',
                       plot_kwargs={'alpha': 0.5}, ylim=(-1, 1))
hp.plot('chr18:6mb-10mb')
hp.show()
# end snippet bloomplot line ylim

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_line_ylim.png'))

# start snippet bloomplot line multi
hp = bloomplot.LinePlot((insulation_scores_1mb, insulation_scores_2mb),
                       style='mid', colors=('cyan', 'magenta'),
                       plot_kwargs={'alpha': 0.5}, ylim=(-1, 1),
                       labels=('1mb', '2mb'))
hp.plot('chr18:6mb-10mb')
hp.show()
# end snippet bloomplot line multi

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_line_multi.png'))

# start snippet bloomplot bar basic
hp = bloomplot.BarPlot((insulation_scores_1mb, insulation_scores_2mb),
                      colors=('cyan', 'magenta'),
                      plot_kwargs={'alpha': 0.5}, ylim=(-1, 1),
                      labels=('1mb', '2mb'))
hp.plot('chr18:6mb-10mb')
hp.show()
# end snippet bloomplot bar basic

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_bar.png'))

# start snippet bloomplot bar boundaries
hp = bloomplot.BarPlot(boundaries_1mb, colors='cyan')
hp.plot('chr18:20mb-30mb')
hp.show()
# end snippet bloomplot bar boundaries

hp.save(os.path.join(bloom_base, 'docsrc/api/plot/images/plot_bar_boundaries.png'))