import numpy as np

# data size
ndays=10000

# generate input for random set / time labels (days)
days=np.arange(1,ndays+1,1)

# generate training data
print('... generate training data')
rng = np.random.default_rng(22)
# T with normal distribution
T = rng.normal(6., 1., days.size)
# Td with normal distribution
Td = rng.normal(5.9, 1.5, days.size)
# wind speed with Weibull distribution
wind = rng.weibull(1., days.size)

# maximize Td in T
maskt = (Td >= T)
Td[maskt] = T[maskt]

# estimate fog: T = Td and wind <= 0.8
print('... estimate fog via physical model')
wind_threshold = 0.8
maskwind = (wind > wind_threshold)
no=np.zeros_like(T)
yes=np.ones_like(T)
fog=np.copy(no)
fog[maskt] = yes[maskt]
fog[maskwind] = no[maskwind]

# save data to file
data = f'training_data.txt'
print('... writing training data to file:', data)
with open(data, "w") as text_file:
    for jt in np.arange(T.size):
          print(f'{days[jt]:>6.3f} '
                f'{T[jt]:>6.3f} '
                f'{Td[jt]:>6.3f}',
                f'{wind[jt]:>6.3f}',
                f'{fog[jt]:>6.3f}',
                file=text_file)




