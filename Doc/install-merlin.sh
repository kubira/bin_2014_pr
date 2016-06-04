#!/bin/bash

# Stažení Python 3.4.0
wget https://www.python.org/ftp/python/3.4.0/Python-3.4.0.tgz

# Rozbalení Python
tar -xf Python-3.4.0.tgz

# Instalace Python
cd Python-3.4.0
./configure --prefix=$HOME/local
make install
cd ..

# Úklid po Python instalaci
rm -rf Python-3.4.0
rm Python-3.4.0.tgz

# Konfigurace cest
echo "" >> ~/.profile
echo "# xkubis03 BIN projekt instalace" >> ~/.profile
echo "export PATH=\$PATH:\$HOME/local/bin" >> ~/.profile
echo "export PYTHONPATH=\$HOME/local/lib/python3.4/site-packages:\$PYTHONPATH" >> ~/.profile
echo "export LD_LIBRARY_PATH=/usr/local/share/OpenMPI/lib:\$LD_LIBRARY_PATH" >> ~/.profile
source ~/.profile

# Stažení mpi4py
wget https://mpi4py.googlecode.com/files/mpi4py-1.3.1.tar.gz

# Rozbalení mpi4py
tar -xf mpi4py-1.3.1.tar.gz

# Instalace mpi4py
cd mpi4py-1.3.1
MPICC=/usr/local/share/OpenMPI/bin/mpicc python3.4 setup.py install
cd ..

# Úklid po mpi4py instalaci
rm -rf mpi4py-1.3.1
rm mpi4py-1.3.1.tar.gz

# Stažení numpy
wget http://freefr.dl.sourceforge.net/project/numpy/NumPy/1.8.1/numpy-1.8.1.tar.gz

# Rozbalení numpy
tar -xf numpy-1.8.1.tar.gz

# Instalace numpy
cd numpy-1.8.1
python3.4 setup.py install
cd ..

# Úklid po numpy instalaci
rm numpy-1.8.1.tar.gz
rm -rf numpy-1.8.1

# Konec
echo "Instalace dokončena"
echo "Prosím, spusťte příkaz \"source ~/.profile\" pro načtení konfigurace"
