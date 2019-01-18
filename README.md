_I have been working on other projects recently and haven't had the stamina to keep things up to date. I may take up maintainership  again in the future._



```
____  ____ ________        __  
\   \/   //  _____/____  _/  |_
 \      / \____  \\__  \/_    _/
 /      \ /       \/ __ \_|  | 
/___/\   /_______ (____  /|_ | 
      \___\     \/     \/   \|      
```
XSat is a fast floating-point constraint solver. Evaluated on 34 representative
SMT Competition benchmarks, XSat provides consistent satisfiability results as
MathSat and Z3, and an average of more than 700X performance speedup. 

DISCLAIMER: XSat currently does _not_ supports all QF\_FP operations. This
version supports the arithmetic operations of the QF\_FP (Quantifier-Free
Floating-Point) theory, including: fp.leq, fp.lt, fp.geq, fp.gt, fp.eq, fp.neg,
fp.add, fp.mult, fp.sub and fp.div.  

See [Fu and Su's CAV'16
paper](http://zhoulaifu.com/wp-content/papercite-data/pdf/xsat.pdf) for the
algorithm and implementation details.




Dependencies 
-------------------
- python 2.7
- python packages: python-dev, sympy, numpy, scipy
- Clang (preferred, which allows you to use the `-fbracket-depth` option, see below), or gcc
- Z3 (I used its 4.5.0 version for parsing SMT2 files) 


Running XSat
----------------------
Note:

1. To resolve runtime dependencies, you probably need to set environment variables (such as LD\_LIBRARY\_PATH or PYTHONPATH) or variables defined in `Makefile`. 

2. The option "-fbracket-depth" is from Clang. Gcc does not have that option. The option is to deal with situations where the generated C file gets many brackets. You can disable that option in Makefile and you should be fine most of the time. Meanwhile, I plan to optimize a bit the algorithm (there is large room!) to avoid generating too many brackets, so hopefully, that option can be safely removed in the future.  

#### Running from the source

Consider a benchmark constraint located at `Benchmarks/div3.c.50.smt2`.  The first command below compiles the constraint into a C shared object. The second command below invokes an external stochastic optimization backend to solve the constraint.

```bash
$ make IN=Benchmarks/div3.c.50.smt2
$ python xsat.py 
```

You can type `make helloworld` as a shortcut.  

Note: the second command above can be supplemented with a range of options.  Use "--help"  to get the list of command line options. In particular, the "--debug" option is set on by default, meaning that you will see verbose output. To get only the satisfiability result, supplement the second command with "--bench" option.



#### Running from the docker

Note: The docker is provided for your convenience, but code maintenance is only on the source. 

First, get the image and start the container:
```bash
docker pull martinvelez/xsat
docker run -it martinvelez/xsat:latest bash
```
Then, run XSat from  the source.

Testing XSat
--------------
```bash
$ python test_benchmarks.py 
```
This command tests XSat on a suite of the 34 benchmarks used in the [paper, table 1](http://zhoulaifu.com/wp-content/papercite-data/pdf/xsat.pdf). To test only a subset of these benchmarks, use `python test_benchmarks.py --quick <n>` where `n` is a positive integer. With n = 10, the command  tests the 10th, 20th and 30th benchmark of the suite.

#### Expected results
```
$ time python test_benchmarks.py
(1) Working on Benchmarks/div2.c.30.smt2
   Compiling ...
   Solving ...
   ==> sat [Expected]
(2) Working on Benchmarks/mult1.c.30.smt2
   Compiling ...
   Solving ...
   ==> sat [Expected]
...
...
(28) Working on Benchmarks/test_v5_r10_vr10_c1_s21502.smt2
   Compiling ...
   Solving ...
   ==> unsat [Expected]
(29) Working on Benchmarks/sin2.c.10.smt2
   Compiling ...
   Solving ...
   ==> sat [Expected]
(30) Working on Benchmarks/div2.c.50.smt2
   Compiling ...
   Solving ...
   ==> sat [Expected]
(31) Working on Benchmarks/mult1.c.50.smt2
   Compiling ...
   Solving ...
   ==> sat [Expected]
(32) Working on Benchmarks/div3.c.50.smt2
   Compiling ...
   Solving ...
   ==> sat [Expected]
(33) Working on Benchmarks/mult2.c.50.smt2
   Compiling ...
   Solving ...
   ==> sat [Expected]
(34) Working on Benchmarks/div.c.50.smt2
   Compiling ...
   Solving ...
   ==> sat [Expected]

real	1m53.170s
user	4m55.804s
sys	    0m24.029s

```
I recently found that XSat sometimes gave incorrect results for `sin2.c.10.smt2` (\#29 above). It can be a new bug, or week parameter settings (e.g. insufficient iteration numbers), but I do not have time to investigate on this at this moment.  
