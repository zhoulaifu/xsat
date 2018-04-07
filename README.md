
    ____  ___                __   
    \   \/  / ___________  _/  |_ 
     \     / /  ___/\__  \/_    _/
     /     \ \___ \  / __ \_|  |  
    /__/\   \/___  >(____  /|_ |  
         \___\   \/      \/   \|   



Xsat is a fast floating-point constraint solver. Evaluated on 34 representative
SMT Competition benchmarks, XSat provides consistent satisfiability results as
MathSat and Z3, and an average of more than 700X performance speedup. Xsat
currently supports the arithmetic operations of the QF\_FP (Quantifier-Free
Floating-Point) theory, including: fp.leq, fp.lt, fp.geq, fp.gt, fp.eq, fp.neg,
fp.add, fp.mult, fp.sub and fp.div. See details in [Fu and Su's CAV'16
paper](http://zhoulaifu.com/wp-content/papercite-data/pdf/xsat.pdf).




Dependencies 
-------------------
- python 2.7
- python packages: python-dev, sympy, numpy, scipy
- gcc
- [Z3](https://github.com/Z3Prover/z3/releases/tag/z3-4.5.0) (Note: Z3 is used as a parser of SMT2 files) 


Running Xsat
----------------------
To resolve runtime dependencies, you probably need to set environment variables (such as LD\_LIBRARY\_PATH or PYTHONPATH) or variables defined in `Makefile`. 


#### Running from the source

Consider a benchmark constraint located at `Benchmarks/div3.c.50.smt2`.  The first command below compiles the constraint into a C shared object. The second command below invokes an external stochastic optimization backend to solve the constraint.

```bash
$ make IN=Benchmarks/div3.c.50.smt2
$ python xsat.py 
```

You can type `make helloworld` as a shortcut.  

Note: the second command above can be supplemented with a range of options.  Use "--help"  to get the list of command line options. In particular, the "--debug" option is set on by default, meaning that you will see verbose output. To get only the satisfiability result, supplement the second command with "--bench" option.



#### Running from the docker

First, get the image and start the container:
```bash
docker pull martinvelez/xsat
docker run -it martinvelez/xsat:latest bash
```
Then, run Xsat from  the source.


Testing Xsat
--------------
```bash
$ python test_benchmarks.py 
```
This command tests Xsat on a suite of the 34 benchmarks used in the [paper, table 1](http://zhoulaifu.com/wp-content/papercite-data/pdf/xsat.pdf). To test only a subset of these benchmarks, use `python test_benchmarks.py --quick <n>` where `n` is a positive integer. With n = 10, the command  tests the 10th, 20th and 30th benchmark of the suite.

