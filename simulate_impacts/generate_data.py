import powerlaw as pl
import os

dir = os.path.dirname(os.path.realpath(__file__))

print(dir)
#create power law distribution using minimum crater diameter of 10, using integers (discrete)
distribution = pl.Power_Law(xmin=10, xmax=500, parameters=[2.5], discrete=True)

#generate random numbers from the theoretical distribution

data = distribution.generate_random(10000, estimate_discrete=True)

datafile = open(dir + "\data.txt", 'w')
for datum in data:
    datafile.write("%d\n" % int(datum))