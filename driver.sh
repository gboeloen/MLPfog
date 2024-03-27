#!/usr//bin/bash

#-------------------------- preparations -----------------------

# default is to do nothing
[[ ${exp}    == '' ]] && exp=exp
[[ ${verify} == '' ]] && verify=0
[[ ${plot}   == '' ]] && plot=0

# read flags in case of interactive execution
while getopts e:v:p: option ; do
   case $option in
   e) exp=$OPTARG ;;
   v) verify=$OPTARG ;;
   p) plot=$OPTARG ;;
   esac
done

#------------------------ define functions ---------------------

# check argument
checkargs () {
  exp=$1
  verify=$2
  plot=$3
  if [[ (${verify} != '0' && ${verify} != '1') \
         || \
         (${plot} != '0' && ${plot} != '1') ]]
  then
    echo
    echo "One of the arguments 'verify', 'plot' are not correct!"
    echo "You can run this script e.g. as:"
    echo "  driver.sh -e exp+your_added_id (default: exp) -v 0/1 -p 0/1"
    echo
    exit
  fi
  begin=`echo ${exp} |cut -c 1-3`
  if [[ ${begin} != 'exp' ]] ; then
    echo
    echo "Experiment name should start with the characters 'exp'!"
    echo "You can run this script e.g. as:"
    echo "  driver.sh -e exp+your_added_id (default: exp) -v 0/1 -p 0/1"
    echo
    exit
  fi
  if [[ ${exp} == 'exp' ]] ; then
    echo
    echo "Argument '-e your_exp_name' is not set"
    echo " --> default exp name 'exp' used."
    echo
  fi
  if [[ (${verify} == '0' || ${plot} == '0') ]] ; then
    echo
    echo "Verification & plotting is switched off."
    echo "To switch them on, run as:"
    echo "  driver.sh -v 1 -p 1"
    echo
  fi

}
#--------------------------- main part --------------------------

# define base dir
expbase=$PWD

# check argument
checkargs ${exp} ${verify} ${plot}

# load python environment 
cd ./myvenv
source load_myvenv.sh

# create experiment dir
if [[ -d ${expbase}/${exp} ]] ; then
  echo
  echo "Experiment ${expbase}/${exp} already exist --> exit"
  echo
  exit
else
  cp -Rp ${expbase}/src ${expbase}/${exp}
fi

# go to exp dir
cd ${expbase}/${exp}

# clean
rm -f *.txt *.png clf.dat

# generate training data
python generate_training_data.py

# do training
python train_mlp_model.py

# generate test data
python generate_test_data_set.py

# do prediction with physical model (truth)
python predict_set_physical_model.py

# do prediction with MLP (ANN)
python predict_set_mlp_model.py

# verify
if [[ $verify == 1 ]] ; then
   python verify_set.py
fi

# plot
if [[ $plot == 1 ]] ; then
   python plot_training_data.py
   python plot_test_data.py
   python plot_result_physical.py
   python plot_result_mlp.py
   python plot_result_mlp_verify.py
fi
