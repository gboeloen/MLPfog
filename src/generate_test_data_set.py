import numpy as np

# data size
ndays=10000

# generate input for random set / time labels (days)
days=np.arange(1,ndays+1,1)

# generate several realizations (periods) in a loop
nperiods=10
for jp in np.arange(nperiods):

   print('realization:', jp)

   # generate test data
   print('... generate test data')
   rng = np.random.default_rng(jp)
   # T with normal distribution
   T = rng.normal(6., 1., days.size)
   # Td with normal distribution
   Td = rng.normal(5.5, 1.2, days.size)
   # wind speed with Weibull distribution
   wind = rng.weibull(1., days.size)

   # maximize Td in T
   mask = (Td >= T)
   Td[mask] = T[mask]
   
   # save data to file
   data = f'test_data_'+str(jp)+'.txt'
   print('... writing training data to file:', data)
   with open(data, "w") as text_file:
       for jt in np.arange(T.size):
             print(f'{days[jt]:>6.3f} '
                   f'{T[jt]:>6.3f} '
                   f'{Td[jt]:>6.3f}',
                   f'{wind[jt]:>6.3f}',
                   file=text_file)




