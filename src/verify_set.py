import numpy as np
import matplotlib.pyplot as plt

# generate several realizations (periods) in a loop
nperiods=10
aperiods=np.zeros(nperiods)
ah=np.zeros(nperiods)
af=np.zeros(nperiods)
asedi=np.zeros(nperiods)
for jp in np.arange(nperiods):

   print('realization:', jp)

   # fill period IDs
   aperiods[jp] = jp+1

   # read result of physical model
   print('... read result of physical model')
   data_phy=np.loadtxt('result_phy_'+str(jp)+'.txt')
   mydates=data_phy[:,0]
   fog_phy=data_phy[:,4]
   
   # read result of mlp model
   print('... read result of mlp model')
   data_mlp=np.loadtxt('result_mlp_'+str(jp)+'.txt')
   fog_mlp=data_mlp[:,4]

   # contingency table notation:
   ##########################################
   # #                  obs (phy)
   #   #
   #     ###################################
   #     #           yes        no
   #     # 
   #     #  yes       a         b
   #fcst #  
   #(mlp)#
   #     #  no        c         d
   #     #   
   #     #   
   ##########################################
   
   # calculate a: hits
   #           b: false alarms
   #           c: missed events
   #           d: correct noevents
   test_a_and_d = (fog_mlp == fog_phy)
   test_b_and_c = (fog_mlp != fog_phy)
   test_a = (fog_phy[test_a_and_d] == 1.)
   test_b = (fog_phy[test_b_and_c] != 1.)
   test_c = (fog_phy[test_b_and_c] == 1.)
   test_d = (fog_phy[test_a_and_d] != 1.)
   a=test_a.sum()
   print('... calculate hits:', a)
   b=test_b.sum()
   print('... calculate false alarms:', b)
   c=test_c.sum()
   print('... calculate missed events:', c)
   d=test_d.sum()
   print('... calculate correct no events:', d)


   # calculate POD & FAR
   print('... calculate POD and FAR')
   # H or POD
   h=a/(a+c)
   # F or FAR
   f=b/(b+d)

   # fill POD & FAR arrays
   ah[jp]    = h
   af[jp]    = f

   # calculate SEDI (symmetix extremal dependence index)
   # Ferro and Stephenson, 2011, Weather and Forcasting
   print('... calculate SEDI')
   h = np.min([h,0.9999999999])
   h = np.max([h,0.0000000001])
   f = np.min([f,0.9999999999])
   f = np.max([f,0.0000000001])
   nom   = np.log(f)-np.log(h)-np.log(1.-f)+np.log(1.-h)
   denom = np.log(f)+np.log(h)+np.log(1.-f)+np.log(1.-h)
   sedi=nom/denom
   
   # fill SEDI arrays
   asedi[jp] = sedi

figname="pod_far.png"
print('... plot POD and FAR to file:', figname)
# set font size generally
plt.rcParams['font.size']=18
#-- create figure
fig = plt.figure(dpi=100, figsize=[8.2, 6.5])
ax1 = fig.subplots()
#-- x and y labels
plt.xlabel('Realizations')
plt.ylabel('POD & FAR')
ax1.set_xlim(0,nperiods+1)
ax1.set_ylim(-0.1,1.1)
#-- set xtics
ax1.set_xticks(np.arange(1,nperiods+1, step=1))
#-- set ytics
ax1.set_yticks(np.arange(0,1.1, step=0.1))
# legend
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles, labels)
# plot grid
lgrid = ax1.grid(color='grey', linestyle='-.', linewidth=0.2)
# plot POD & FAR
lplot1, = ax1.plot(aperiods,ah,color='b', marker='o', linestyle='solid', label='POD')
lplot2, = ax1.plot(aperiods,af,color='r', marker='s', linestyle='solid', label='FAR')
# plot legend
llegend = plt.legend(handles=[lplot1, lplot2],fontsize='small')
lgrid1 = ax1.grid(color='grey', linestyle='-.', linewidth=0.2)
# save fig
plt.savefig(figname, format="png", bbox_inches='tight')

figname="sedi.png"
print('... plot SEDI to file:', figname)
# set font size generally
plt.rcParams['font.size']=18
#-- create figure
fig = plt.figure(dpi=100, figsize=[8.2, 6.5])
ax1 = fig.subplots()
#-- x and y labels
plt.xlabel('Realizations')
plt.ylabel('SEDI')
ax1.set_xlim(0,nperiods+1)
ax1.set_ylim(-0.1,1.1)
#-- set xtics
ax1.set_xticks(np.arange(1,nperiods+1, step=1))
#-- set ytics
ax1.set_yticks(np.arange(0,1.1, step=0.1))
# legend
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles, labels)
# plot grid
lgrid = ax1.grid(color='grey', linestyle='-.', linewidth=0.2)
# plot POD & FAR
lplot1, = ax1.plot(aperiods,asedi,color='b', marker='o', linestyle='solid', label='SEDI')
# plot legend
llegend = plt.legend(handles=[lplot1],fontsize='small')
lgrid1 = ax1.grid(color='grey', linestyle='-.', linewidth=0.2)
# save fig
plt.savefig(figname, format="png", bbox_inches='tight')
