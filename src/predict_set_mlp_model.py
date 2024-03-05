import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import pickle

# set if scaling to be done
doscaling=False

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
   
   # define features
   print('... define features')
   X=data[:,1:4]

   # scale features
   if doscaling:
       print('... scale features')
       scaler = StandardScaler()
       scaler.fit(X)
       X = scaler.transform(X)
   
   # load mlp classifier from file
   fname_clf = "clf.dat"
   with open(fname_clf, 'rb') as file:
       clf = pickle.load(file)
   
   # estimate fog (verification on training data)
   print('... estimate fog via mlp classifier')
   fog_mlp_verify = clf.predict(X)
   
   # save result to file
   data = f'result_mlp_'+str(jp)+'.txt'
   print('... writing result to file:', data)
   with open(data, "w") as text_file:
       for jt in np.arange(T.size):
             print(f'{mydates[jt]:>6.3f} '
                   f'{T[jt]:>6.3f} '
                   f'{Td[jt]:>6.3f}',
                   f'{wind[jt]:>6.3f}',
                   f'{fog_mlp_verify[jt]:>6.3f}',
                   file=text_file)

