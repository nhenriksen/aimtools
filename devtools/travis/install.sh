### If you need to do a fresh install, enable following
#rm -rf $HOME/miniconda

### Regular install, check for cached first.
if [ -d "$HOME/miniconda" ]; then
    export PATH="$HOME/miniconda/bin:$PATH"
    conda list
    pip list
else
    if [[ "$TRAVIS_PYTHON_VERSION" == "2.7" ]]; then
        wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O miniconda.sh;
    else
        wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
    fi
    bash miniconda.sh -b -p $HOME/miniconda
    export PATH="$HOME/miniconda/bin:$PATH"
    conda config --add channels omnia --add channels conda-forge
    conda create -y -n myenv python=$TRAVIS_PYTHON_VERSION
    conda install -y -n myenv numpy scipy pandas parmed pytest pytest-cov codecov
fi

source activate myenv
python --version
conda list
