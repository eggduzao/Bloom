# start snippet oe setup
import bloom
import matplotlib.pyplot as plt
import bloom.plotting as bloomplot

hic_500kb = bloom.load("output/hic/binned/bloom_example_500kb.hic")
# end snippet oe setup

hic_500kb.close()
# start snippet oe append
hic_500kb = bloom.load("output/hic/binned/bloom_example_500kb.hic", mode='a')
# end snippet oe append

# start snippet alternative cooler
hic_500kb = bloom.load("architecture/other-hic/bloom_example.mcool@500kb")
# end snippet alternative cooler

# start snippet alternative juicer
hic_500kb = bloom.load("architecture/other-hic/bloom_example.juicer.hic@500kb")
# end snippet alternative juicer

# start snippet oe basic
intra_expected, intra_expected_chromosome, inter_expected = hic_500kb.expected_values()
# end snippet oe basic

# start snippet oe ddplot
# obtain bin distances
bin_size = hic_500kb.bin_size
distance = list(range(0, bin_size * len(intra_expected_chromosome['chr19']), bin_size))

# plot expected values
fig, ax = plt.subplots()
plt.plot(distance, intra_expected_chromosome['chr19'])
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel("Distance")
ax.set_ylabel("Average contacts")
plt.show()
# end snippet oe ddplot
fig.savefig('../docsrc/api/analyse/images/oe_500kb.png')
plt.close(fig)

# start snippet oe ddbuiltin
ax = bloomplot.distance_decay_plot(hic_500kb, chromosome='chr18', color='mediumturquoise')
# end snippet oe ddbuiltin
ax.figure.savefig("../docsrc/api/analyse/images/oe_500kb_builtin.png")
plt.close(ax.figure)


# start snippet oe multi
lowc_hindiii = bloom.load("architecture/other-hic-update/lowc_hindiii_100k_1mb.hic")
lowc_mboi = bloom.load("architecture/other-hic-update/lowc_mboi_100k_1mb.hic")
ax = bloomplot.distance_decay_plot(lowc_hindiii, lowc_mboi, chromosome='chr1',
                                  labels=['HindIII', 'MboI'])
# end snippet oe multi
ax.figure.savefig("../docsrc/api/analyse/images/oe_500kb_multi.png")
plt.close(ax.figure)


# start snippet oe nonorm
intra_expected_nonorm, intra_expected_chromosome_nonorm, inter_expected_nonorm = hic_500kb.expected_values(norm=False)

# obtain bin distances
bin_size = hic_500kb.bin_size
distance = list(range(0, bin_size * len(intra_expected_nonorm), bin_size))

# plot expected values
fig, ax = plt.subplots()
plt.plot(distance, intra_expected_nonorm)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel("Distance")
ax.set_ylabel("Average contacts (not normalised)")
plt.show()
# end snippet oe nonorm
fig.savefig('../docsrc/api/analyse/images/oe_500kb_nonorm.png')
plt.close(fig)


# start snippet oe builtinnonorm
ax = bloomplot.distance_decay_plot(hic_500kb, norm=False)
# end snippet oe builtinnonorm
ax.figure.savefig("../docsrc/api/analyse/images/oe_500kb_builtinnonorm.png")
plt.close(fig)
