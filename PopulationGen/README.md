## eQTL mapping
### calculating hidden factors using PEER: https://github.com/PMBio/peer/wiki/Tutorial; https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3398141/
Modified installation pipeline:
> git clone https://github.com/PMBio/peer
> cd peer/
> mkdir build
> cd build
> cmake -D CMAKE_INSTALL_PREFIX=~/software -D BUILD_PEERTOOL=1 ./..
> conda activate python2 # remember this is an old software and can not support python 3 properly
> conda install -c asmeurer swig # this is an important step, since swig version should not be too new, this is a swig version on 2.0.10
> make
> make install
