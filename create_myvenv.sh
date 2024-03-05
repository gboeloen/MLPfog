#!/bin/bash

# create my venv dir
mkdir ./myvenv
cd ./myvenv

# create virtual env
python3 -m venv $PWD

# activate virtual env
source ./bin/activate
# type 'deactivate' to deactivate

# get latest version of pip
python3 -m pip install --upgrade pip

# install numpy
python3 -m pip install numpy

# install matplotlib
python3 -m pip install matplotlib

# install scikit-learn
python3 -m pip install -U scikit-learn

# create script to load myvenv
echo "#!/bin/bash" > load_myvenv.sh
echo "# activate virtual env" >> load_myvenv.sh
echo "source ./bin/activate" >> load_myvenv.sh
