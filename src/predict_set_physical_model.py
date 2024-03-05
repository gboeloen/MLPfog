import numpy as np

# generate several realizations (periods) in a loop
nperiods=10
for jp in np.arange(nperiods):

   print('realization:', jp)

   # read T & Td & wind
   print('... read T & Td & wind')
   data=np.loadtxt('test_data_'+str(jp)+'.txt')
   mydates=data[:,0]
   T=data[:,1]
   Td=data[:,2]
   wind=data[:,3]
   
   # estimate fog: T = Td and wind <= 0.8
   print('... estimate fog via physical model')
   wind_threshold = 0.8
   maskt = (Td >= T)
   maskwind = (wind > wind_threshold)
   no=np.zeros_like(T)
   yes=np.ones_like(T)
   fog=np.copy(no)
   fog[maskt] = yes[maskt]
   fog[maskwind] = no[maskwind]

   
   # save result to file
   data = f'result_phy_'+str(jp)+'.txt'
   print('... writing result to file:', data)
   with open(data, "w") as text_file:
       for jt in np.arange(T.size):
             print(f'{mydates[jt]:>6.3f} '
                   f'{T[jt]:>6.3f} '
                   f'{Td[jt]:>6.3f}',
                   f'{wind[jt]:>6.3f}',
                   f'{fog[jt]:>6.3f}',
                   file=text_file)

