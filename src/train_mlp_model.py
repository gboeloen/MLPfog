import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import pickle

# set if scaling to be done
doscaling=False

# set solver
mysolver='adam' # 'lbfgs' or 'adam' or 'sgd'

# set alpha regularization parameter
# alpha small --> allows complex decision boundary
#                 but danger of overfitting
# alpha large --> cures overfitting
#                 but danger of loosing information
#                 (allows only simple decision boundary)
myalpha=1e-5

# set no of hidden layers
myarch=(5, 3, 3)

# set max no. of iterations
mymaxit=500

# read T & Td & wind
print('... read T & Td & wind')
data=np.loadtxt('training_data.txt')
mydates=data[:,0]
T=data[:,1]
Td=data[:,2]
wind=data[:,3]
fog=data[:,4]

# define features
print('... define features')
X=data[:,1:4]

# scale features
if doscaling:
    print('... scale features')
    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)

# define target
print('... define target')
y=fog

# train fog detection
print('... start training')

# set classifier
clf = MLPClassifier(solver=mysolver, alpha=myalpha, 
            max_iter=mymaxit, hidden_layer_sizes=myarch, 
            random_state=1)
# fit regression coefficients
clf.fit(X,y)

# save the mlp classifier to file
fname_save_clf = "clf.dat"
print('... save mlp classifier to file:', fname_save_clf)
with open(fname_save_clf, 'wb') as file:
    pickle.dump(clf, file)

# estimate fog (verification on training data)
print('... estimate fog via mlp (on training data as verification)')
fog_mlp_verify = clf.predict(X)

# save result to file
data = f'result_mlp_verify.txt'
print('... writing result to file:', data)
with open(data, "w") as text_file:
    for jt in np.arange(T.size):
          print(f'{mydates[jt]:>6.3f} '
                f'{T[jt]:>6.3f} '
                f'{Td[jt]:>6.3f}',
                f'{wind[jt]:>6.3f}',
                f'{fog_mlp_verify[jt]:>6.3f}',
                file=text_file)

