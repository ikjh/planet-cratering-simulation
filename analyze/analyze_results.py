import os
import pandas as pd
import matplotlib.pyplot as plt

#read in data
dir = os.path.dirname(os.path.realpath(__file__))
results = pd.read_csv(dir + os.path.sep + "results.txt", header=0)

#create and label graph
fig, ax = plt.subplots(1,1)
fig.suptitle("Number of visible craters as a function of time")
ax.set_xlabel("Time (millions of years)")
ax.set_ylabel("Number of visible craters")
ax.plot(results["time"], results["visible_craters"])

#label point of saturation
y_max = max(results["visible_craters"])
print(y_max)
x_pos = list(results["visible_craters"]).index(y_max)
x_max = results["time"][x_pos]
ax.annotate(text='', xy= (x_max, y_max - 5), xytext=(x_max+4, y_max),
    arrowprops=dict( facecolor ='black', shrink= 0.05))

#save and display
plt.savefig(dir + os.path.sep + 'plot2.png')
plt.show()
