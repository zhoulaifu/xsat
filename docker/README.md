# XSat: A Fast Floating-Point Satisfiability Solver

XSat is a very fast satisfiability solver for constraint solving in the
quantifier-free floating-point theory.  

The design and implementation of this solver was described in detail in a paper
published in the Computer Aided Verification 2016
[proceedings](http://i-cav.org/2016/accepted-papers/).  You can also read a
draft [here](http://zhoulaifu.com/wp-content/papercite-data/pdf/xsat.pdf).

## Installation

### Simple Method: Get the Docker Image and Run a container.

Docker is a tool that lets you download packaged applications and execute them.
I use Docker Community Edition
(https://www.docker.com/community-edition#/download). 

Get the image and start the container.

```
docker pull martinvelez/xsat
docker run -it martinvelez/xsat:latest bash
```

Once inside the container, at the bash prompt, compile the input smt2 file, and
then run *xsat.py*. 

```
xsat@3dcc856b7520:~$ make compile IN=mytest.smt2
xsat@3dcc856b7520:~$ python xsat.py
```

*mytest.smt2* - *mytest4.smt2* are sample input files.  Write your own.

### Complex Method: Install and configure all dependencies manually.

#### Dependencies

* gcc 4.8.4 (C compiler)
* Python 2.7.6
* Pythoh.h (from CPython)
* Z3 4.5.0
	* Provides an SMT2 parser.
	* Source code at [https://github.com/Z3Prover/z3.git](https://github.com/Z3Prover/z3.git).
* Python libraries
	* sympy
	* numpy
	* scipy

##### Building Z3

The following instructions get z3 and build it on your machine.  The libraries
are not installed.  They are left in the **build** directory.

Download the source code, and enter directory.
```bash
git clone https://github.com/Z3Prover/z3.git
cd z3
```

From within the z3 folder, run the **mk_make.py** script.
```bash
python scripts/mk_make.py --python
```

Switch into the **build** folder.  Execute the **make** command.
```bash
cd build
make
```

Finally, you need to set two environment variables.  If you do not set this,
then the **xsat.py** will not work.
```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/marvelez/github/z3/build/python
export PYTHONPATH=/home/marvelez/github/z3/build/python/
```


## Example Run
-----------------------

```bash
xsat@3dcc856b7520:~$ make compile IN=mytest.smt2
xsat@3dcc856b7520:~$ python xsat.py
```

Step 1 first generates foo.c corresponding to the provided .smt2 file,  and then compiles it with different xsat.h located in include/.

Step 2 can be supplemented with options. Note that the "--debug" option is set on by default.

The most important files in the repo are:

* xsat.py: The main code of the XSat's minimization part.  
* xsat_gen.py: The main code of the XSat's transformation part from .smt2 to
.c.  It can be either run by itself, or through a Makefile.
* Makefile: shortcuts for running xsat\_gen.py. To run it on your local
machine, you need to change some path variables in this file.   

* include/ : directory which includes various xsat.h files. Each xsat.h is a
configuration of a "representing function" (see the paper).
* Bench/, Bench2/, and other directories started with "Bench": benchmark programs
* logo.txt: Xsat's logo

## Usage
-----------------------

```bash
usage: Xsat [-h] [-v] [--niter NITER] [--nStartOver NSTARTOVER]
	[--method {powell,slsqp,cg,l-bfgs-b,cobyla,tnc,bfgs,nelder-mead,noop_min}]
	[--showTime] [--showResult] [--stepSize STEPSIZE]
	[--round2_stepsize ROUND2_STEPSIZE] [--verify] [--verify2]
	[--showModel] [--showSymbolTable] [--showConstraint]
	[--showVariableNumber] [--command_compilation COMMAND_COMPILATION]
	[--startPoint STARTPOINT] [--round2_threshold ROUND2_THRESHOLD]
	[--round3_threshold ROUND3_THRESHOLD] [--multi MULTI]
	[--round2_niter ROUND2_NITER] [--round3_niter ROUND3_NITER]
	[--round3_stepsize ROUND3_STEPSIZE] [--suppressWarning] [--debug]
	[--printModel] [--bench] [--genOnly]
```

Details on the usage can be found with `python xsat.py -h`.

## SMT-COMP
-----------------------

See [Wiki Page](https://bitbucket.org/zhoulaifu/xsat_implem/wiki/SMT-COMP).
