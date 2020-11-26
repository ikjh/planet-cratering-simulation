import os
import powerlaw.powerlaw as pl

#create power law distribution using minimum crater diameter of 10, using integers (discrete)
distribution = pl.Power_Law(xmin=10, xmax=500, parameters=[2.5], discrete=True)

#generate random numbers from the theoretical distribution
data = distribution.generate_random(10000, estimate_discrete=True)

#export results to file in same directory as this file
dir = os.path.dirname(os.path.realpath(__file__))
print(dir)

#discard bugged values, write clean values to file
datafile = open(dir + os.path.sep + "data.txt", 'w+')
for datum in data:
    if int(datum) <= 500:
        datafile.write("%d\n" % int(datum))