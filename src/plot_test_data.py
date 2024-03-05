import numpy as np
import matplotlib.pyplot as plt

# open file
f1 = open('test_data_0.txt', 'r')
# initialize lists
ldate = []
lt = []
ltd = []
lwind = []
lfog = []
# loop over lines and extract variables of interest
for line in f1:
    line = line.strip()
    columns = line.split()
    date   = float(columns[0])
    t      = float(columns[1])
    td     = float(columns[2])
    wind   = float(columns[3])
    # save vars to lists
    ldate.append(date)
    lt.append(t)
    ltd.append(td)
    lwind.append(wind)
f1.close()

# calculate distributions
count_t, bins_t, ignored_t = plt.hist(lt)
count_td, bins_td, ignored_td = plt.hist(ltd)
count_wind, bins_wind, ignored_wind = plt.hist(lwind)

# FULL FIG
# set font size generally
plt.rcParams['font.size']=18
#-- create figure
fig = plt.figure(dpi=100, figsize=[8.2, 6.5])
ax1 = fig.subplots()
#-- x and y labels
plt.xlabel('Time instances')
plt.ylabel('Values')
ax1.set_ylim(-1,10)
#-- set xtics
#xticks(np.array([7,27,47,67,87]), ('280', '300', '320', '340', '360'))
#ax1.set_xticks(np.arange(280,370, step=10))
#-- set ytics
#yticks(np.arange(-20,20, step=1), ('10', '20', '30', '40', '50', '60', '70'))
ax1.set_yticks(np.arange(-1,10, step=1))
# legend
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles, labels)
# plot grid
lgrid = ax1.grid(color='grey', linestyle='-.', linewidth=0.2)
# plot zjm mean msgwam
lplot1, = ax1.plot(ldate,lt,color='r', linestyle='solid', linewidth=2.0, label='T')
lplot2, = ax1.plot(ldate,ltd,color='b', linestyle='solid', linewidth=2.0, label='Td')
lplot3, = ax1.plot(ldate,lwind,color='g', linestyle='solid', linewidth=2.0, label='wind')
# set ytics
# plot legend
llegend = plt.legend(handles=[lplot1, lplot2, lplot3],fontsize='small')
lgrid1 = ax1.grid(color='grey', linestyle='-.', linewidth=0.2)
# save fig
plt.savefig("test_data_0.png",format="png", bbox_inches='tight')

# DEMO FIG
# set font size generally
plt.rcParams['font.size']=18
#-- create figure
fig = plt.figure(dpi=100, figsize=[8.2, 6.5])
ax1 = fig.subplots()
#-- x and y labels
plt.xlabel('Time instances')
plt.ylabel('Values')
ax1.set_xlim(0,100)
ax1.set_ylim(-1,10)
#-- set xtics
#xticks(np.array([7,27,47,67,87]), ('280', '300', '320', '340', '360'))
#ax1.set_xticks(np.arange(280,370, step=10))
#-- set ytics
#yticks(np.arange(-20,20, step=1), ('10', '20', '30', '40', '50', '60', '70'))
ax1.set_yticks(np.arange(-1,10, step=1))
# legend
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles, labels)
# plot grid
lgrid = ax1.grid(color='grey', linestyle='-.', linewidth=0.2)
# plot zjm mean msgwam
lplot1, = ax1.plot(ldate,lt,color='r', linestyle='solid', linewidth=2.0, label='T')
lplot2, = ax1.plot(ldate,ltd,color='b', linestyle='solid', linewidth=2.0, label='Td')
lplot3, = ax1.plot(ldate,lwind,color='g', linestyle='solid', linewidth=2.0, label='wind')
# set ytics
# plot legend
llegend = plt.legend(handles=[lplot1, lplot2, lplot3],fontsize='small')
lgrid1 = ax1.grid(color='grey', linestyle='-.', linewidth=0.2)
# save fig
plt.savefig("test_data_0_demo.png",format="png", bbox_inches='tight')

# DISTRIBUTION FIG
# set font size generally
plt.rcParams['font.size']=18
#-- create figure
fig = plt.figure(dpi=100, figsize=[8.2, 6.5])
ax1 = fig.subplots()
#-- x and y labels
plt.xlabel('Values')
plt.ylabel('No. of occurence')
# legend
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles, labels)
# plot grid
lgrid = ax1.grid(color='grey', linestyle='-.', linewidth=0.2)
# plot zjm mean msgwam
lplot1, = ax1.plot(bins_t[:count_t.size], count_t, color='r', linestyle='solid', linewidth=2.0, marker='o', label='T')
lplot2, = ax1.plot(bins_td[:count_td.size], count_td, color='b', linestyle='solid', linewidth=2.0, marker='o', label='Td')
lplot3, = ax1.plot(bins_wind[:count_wind.size], count_wind, color='g', linestyle='solid', linewidth=2.0, marker='o', label='wind')
# set ytics
# plot legend
llegend = plt.legend(handles=[lplot1, lplot2, lplot3],fontsize='small')
# save fig
plt.savefig("test_dist_0.png",format="png", bbox_inches='tight')

