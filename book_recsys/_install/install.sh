#!/bin/bash

GREEN='\033[1;32m'
NC='\033[0m' # No Color

function print_title {
   echo -e "\n\n\n"
   echo -e "${GREEN}############################################################"
   echo '###' $1
   echo -e "############################################################${NC}"
}

############################################################
print_title "create env ..."

conda create --yes -n bkms1_team10 python=3.8
conda activate bkms1_team10

############################################################
print_title "upgrade pip ..."

conda install --yes -c anaconda pip

############################################################
print_title "install Packages ..."

conda install --yes -c conda-forge pyyaml
conda install --yes -c conda-forge gdown
conda install --yes -c conda-forge gzip
conda install --yes -c conda-forge json
conda install --yes -c conda-forge nltk
conda install --yes -c conda-forge wordcloud
conda install --yes -c conda-forge matplotlib
conda install --yes -c conda-forge scikit-learn
conda install --yes -c conda-forge pandas
