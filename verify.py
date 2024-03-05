import numpy as np
import matplotlib.pyplot as plt

# generate several realizations (periods) in a loop
nperiods=10
nexps=10
aperiods=np.zeros((nexps,nperiods))
aexps=np.zeros((nexps,nperiods))
asize=np.zeros((nexps,nperiods)).astype(int)
ah=np.zeros((nexps,nperiods))
af=np.zeros((nexps,nperiods))
asedi=np.zeros((nexps,nperiods))
for je in np.arange(nexps):

   expname = 'exp'+str(je+1)

   print('... verify exp:', expname)

   for jp in np.arange(nperiods):
   
      print('realization:', jp)

      # fill exp IDs
      aexps[je,jp] = je
      if je > 4:
         aexps[je,jp] = aexps[je,jp]-5
   
      # fill period IDs
      aperiods[je,jp] = jp+1
   
      # read result of physical model
      print('... read result of physical model')
      data_phy=np.loadtxt(expname+'/result_phy_'+str(jp)+'.txt')
      fog_phy=data_phy[:,4]
      
      # read result of mlp model
      print('... read result of mlp model')
      data_mlp=np.loadtxt(expname+'/result_mlp_'+str(jp)+'.txt')
      fog_mlp=data_mlp[:,4]

      # get size of training period
      # read training data
      data_tr=np.loadtxt(expname+'/training_data.txt')
      asize[je,jp] = np.int64(data_tr[:,0].size)

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
      ah[je,jp]    = h
      af[je,jp]    = f

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
      asedi[je,jp] = sedi

# calculate mean over periods (realizations)
ahm=np.mean(ah, axis=1)
afm=np.mean(af, axis=1)
asedim=np.mean(asedi, axis=1)

figname="sedi_set.png"
print('... plot SEDI to file:', figname)
# set font size generally
plt.rcParams['font.size']=18
#-- create figure
fig = plt.figure(dpi=100, figsize=[8.2, 6.5])
ax1 = fig.subplots()
#-- title
plt.title('MLP Architecture: (5,3,3)')
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
# plot SEDI
lplot1,  = ax1.plot(aperiods[0,:],asedi[0,:],color='k', linestyle='solid', marker='o', label='SEDI trsize:'+str(asize[0,0]))
lplot2,  = ax1.plot(aperiods[1,:],asedi[1,:],color='b', linestyle='solid', marker='o', label='SEDI trsize:'+str(asize[1,0]))
lplot3,  = ax1.plot(aperiods[2,:],asedi[2,:],color='r', linestyle='solid', marker='o', label='SEDI trsize:'+str(asize[2,0]))
lplot4,  = ax1.plot(aperiods[3,:],asedi[3,:],color='c', linestyle='solid', marker='o', label='SEDI trsize:'+str(asize[3,0]))
lplot5,  = ax1.plot(aperiods[4,:],asedi[4,:],color='m', linestyle='solid', marker='o', label='SEDI trsize:'+str(asize[4,0]))
#lplot6,  = ax1.plot(aperiods[5,:],asedi[5,:],color='k', linestyle='solid', marker='s', label='SEDI trsize:'+str(asize[5,0])+' standardized')
#lplot7,  = ax1.plot(aperiods[6,:],asedi[6,:],color='b', linestyle='solid', marker='s', label='SEDI trsize:'+str(asize[6,0])+' standardized')
#lplot8,  = ax1.plot(aperiods[7,:],asedi[7,:],color='r', linestyle='solid', marker='s', label='SEDI trsize:'+str(asize[7,0])+' standardized')
#lplot9,  = ax1.plot(aperiods[8,:],asedi[8,:],color='c', linestyle='solid', marker='s', label='SEDI trsize:'+str(asize[8,0])+' standardized')
#lplot10, = ax1.plot(aperiods[9,:],asedi[9,:],color='m', linestyle='solid', marker='s', label='SEDI trsize:'+str(asize[9,0])+' standardized')
# plot legend
#llegend = plt.legend(handles=[lplot1, lplot2, lplot3, lplot4, lplot5, lplot6, lplot7, lplot8, lplot9, lplot10],fontsize='small')
llegend = plt.legend(handles=[lplot1, lplot2, lplot3, lplot4, lplot5],fontsize='small')
# save fig
plt.savefig(figname, format="png", bbox_inches='tight')

figname="sedi_trsize.png"
print('... plot SEDI to file:', figname)
# set font size generally
plt.rcParams['font.size']=18
#-- create figure
fig = plt.figure(dpi=100, figsize=[8.2, 6.5])
ax1 = fig.subplots()
#-- title
plt.title('MLP Architecture: (5,3,3)')
#-- x and y labels
plt.xlabel('Training size')
plt.ylabel('SEDI')
ax1.set_ylim(-0.1,1.1)
#-- set xtics
ax1.set_xticks(aexps[0:5,0], ('10^4', '10^3', '10^2', '10^1', '5'))
#-- set ytics
ax1.set_yticks(np.arange(0,1.1, step=0.1))
# legend
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles, labels)
# plot grid
lgrid = ax1.grid(color='grey', linestyle='-.', linewidth=0.2)
# plot SEDI
lplot1,  = ax1.plot(aexps[0:5,0],asedim[0:5],color='b', linestyle='solid',   linewidth=2., marker='o', label='SEDI')
lplot2,  = ax1.plot(aexps[5:10,0],asedim[5:10],color='r', linestyle='solid', linewidth=2., marker='s', label='SEDI standardized')
# plot legend
llegend = plt.legend(handles=[lplot1, lplot2],fontsize='small')
# save fig
plt.savefig(figname, format="png", bbox_inches='tight')

figname="pod_far_trsize.png"
print('... plot POD & FAR to file:', figname)
# set font size generally
plt.rcParams['font.size']=18
#-- create figure
fig = plt.figure(dpi=100, figsize=[8.2, 6.5])
ax1 = fig.subplots()
#-- title
plt.title('MLP Architecture: (5,3,3)')
#-- x and y labels
plt.xlabel('Training size')
plt.ylabel('POD & FAR')
ax1.set_ylim(-0.1,1.1)
#-- set xtics
ax1.set_xticks(aexps[0:5,0], ('10^4', '10^3', '10^2', '10^1', '5'))
#-- set ytics
ax1.set_yticks(np.arange(0,1.1, step=0.1))
# legend
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles, labels)
# plot grid
lgrid = ax1.grid(color='grey', linestyle='-.', linewidth=0.2)
# plot POD & FAR
lplot1,  = ax1.plot(aexps[0:5,0],ahm[0:5],color='b', linestyle='solid',   linewidth=2., marker='o', label='POD')
lplot2,  = ax1.plot(aexps[0:5,0],afm[0:5],color='b', linestyle='dashed',   linewidth=2., marker='s', label='FAR')
lplot3,  = ax1.plot(aexps[5:10,0],ahm[5:10],color='r', linestyle='solid', linewidth=2., marker='o', label='POD standardized')
lplot4,  = ax1.plot(aexps[5:10,0],afm[5:10],color='r', linestyle='dashed', linewidth=2., marker='s', label='FAR standardized')
# plot legend
llegend = plt.legend(handles=[lplot1, lplot2, lplot3, lplot4],fontsize='small')
# save fig
plt.savefig(figname, format="png", bbox_inches='tight')

