# This includes XSat and all of its depencies.

# Set the base image
FROM ubuntu:14.04

# Dockerfile author / maintainer 
LABEL maintainer="marvelez@ucdavis.edu"

# Update and upgrade packages.
RUN DEBIAN_FRONTEND=noninteractive apt-get update 

# Install gcc.
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common gcc gdb vim make 
# root@bc6cc8f37ae0:/usr/src/app# gcc --version
# gcc (Ubuntu 4.8.4-2ubuntu1~14.04.3) 4.8.4

# Install fortran.
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y gfortran

# Install wget.
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y wget

# Install pip packages and dependecies.
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential python-dev python-pip 
RUN apt-get install -y libatlas-base-dev
RUN pip install sympy
RUN pip install numpy 
RUN pip install scipy 

# Create user.
RUN useradd -ms /bin/bash xsat
USER xsat
WORKDIR /home/xsat

ENV MYPYTHON=/usr/bin/python
#export PYTHONINC=$HOME/bin/python/include/python2.7
ENV PYTHONINC /usr/include/python2.7/
#export PYTHONLIB=$HOME/bin/python/lib
ENV PYTHONLIB /usr/lib/python2.7/
#export LD_LIBRARY_PATH=$HOME/bin/python/lib
ENV LD_LIBRARY_PATH /usr/lib/python2.7/

# Build and install Z3.
RUN wget https://github.com/Z3Prover/z3/archive/z3-4.5.0.tar.gz
RUN tar xvzf z3-4.5.0.tar.gz
WORKDIR /home/xsat/z3-z3-4.5.0
RUN python scripts/mk_make.py --python
WORKDIR /home/xsat/z3-z3-4.5.0/build
RUN make
USER root
RUN make install
WORKDIR /home/xsat
USER xsat


# Finally, you need to set two environment variables.  If you do not set this,
# then the **xsat.py** will not work.
# ```bash
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/marvelez/github/z3/build/python
# export PYTHONPATH=/home/marvelez/github/z3/build/python/
# ```

ENV PYTHONPATH /home/xsat/z3-z3-4.5.0/build/python

# Add XSat files.
ADD xsat_gen.py /home/xsat/
ADD xsat.py /home/xsat/
ADD mytest.smt2 /home/xsat/
ADD mytest2.smt2 /home/xsat/
ADD mytest3.smt2 /home/xsat/
ADD mytest4.smt2 /home/xsat/
ADD Makefile /home/xsat/
ADD Makefile.verbose /home/xsat/
ADD debug.py /home/xsat/
ADD include /home/xsat/include
ADD README.md /home/xsat/
