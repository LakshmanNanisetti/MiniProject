import numpy
data = numpy.random.random(100)
bins = numpy.linspace(0, 1, 10)
digitized = numpy.digitize(data, bins)
bin_means = [data[digitized == i].mean() for i in range(1, len(bins))]
bin_means = (numpy.histogram(data, bins, weights=data)[0] /
             numpy.histogram(data, bins)[0])
