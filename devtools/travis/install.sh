export PATH=$HOME/miniconda3/bin:$PATH

conda config --add channels omnia --add channels conda-forge

#conda install -y openmm

conda create -y -n myenv python=$PYTHON_VERSION \
      numpy scipy pandas parmed pytest pytest-cov codecov

#conda install -y -n myenv \
#      ambertools=17.0 -c http://ambermd.org/downloads/ambertools/conda/

#conda install -y -n  parmed

#pip install codecov
source activate myenv
python --version

