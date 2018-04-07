#!/usr/bin/env python

############################
###Started on 12/11/2015
###########################
import sympy
import z3
import numpy as np
import scipy.optimize as op
import argparse
import sys, os
import time
import collections
import subprocess
import multiprocessing as mp
import warnings
import struct
import cPickle as pickle

DEBUG=False
def noop_min(fun, x0, args, **options):
    return op.OptimizeResult(x=x0, fun=fun(x0), success=True, nfev=1)

def _get_template():

    template ="""#include <Python.h>
#include "xsat.h"

static PyObject* R(PyObject* self, PyObject *args){
  
  double %(x_vars)s;
  PyArg_ParseTuple(args,"%(x_types)s", %(x_refs)s);
  %(x_body)s
  return Py_BuildValue("d",%(x_expr)s);

}

static PyMethodDef methods[] = {
  {"R", R, METH_VARARGS},
  {NULL, NULL}
};

PyMODINIT_FUNC
 initfoo()
{
  PyObject* module= Py_InitModule("foo", methods);
  PyModule_AddIntConstant(module, "dim", %(x_dim)s);
}
"""
    return template

class Sort:
    UNKNOWN='unknown'
    Float32 = 'float32'
    Float64 = 'float64'
    Real='real'
    Int='int'


def verify_solution(ez, X_star,symbolTable,printModel=False):
    assert isinstance(symbolTable, collections.OrderedDict)
    assert isinstance(ez, z3.ExprRef)
    assert isinstance(res, op.OptimizeResult)
    assert len(symbolTable)==X_star.size
    model=[]
    # (sympy.Symbol('x'), 
    for (s,val) in zip(symbolTable.items(), X_star): 
        var, sort = s[0],s[1]
        if sort == Sort.Float32:
            var_z3=z3.FP(str(var),z3.Float32())
            val_z3=z3.FPVal(val,z3.Float32())
        elif sort == Sort.Float64:
            var_z3=z3.FP(str(var),z3.Float64())
            val_z3=z3.FPVal(val,z3.Float64())
        else:
            raise NotImplementedError("Unexpected type %s" %sort)            
        model.append((var_z3,val_z3))
    if printModel:
        print "model: "
        print model
    return _is_true(z3.simplify(z3.substitute(ez, *model)))
    
def _getSort(expr_z3):
    assert isinstance(expr_z3, z3.ExprRef)
    if expr_z3.sort()==z3.Float32():
        return Sort.Float32
    if expr_z3.sort()==z3.Float64():
        return Sort.Float64
    if expr_z3.sort()==z3.RealSort():
        return Sort.Real
    if expr_z3.sort()==z3.IntSort():
        return Sort.Int
    return Sort. UNKNOWN 

def var_name(expr_z3):
    return "_t_"+str(expr_z3.get_id())


def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text
def rename_var(var):
    reps = {':':'_', '@':'_', '|':'_',"#":'_',"!":"_"}
    return replace_all(var,reps)


def _gen(expr_z3,symbolTable,cache,result):


    ###Leaf: var
    if _is_variable(expr_z3):
        if DEBUG: print "-- Branch _is_variable with ", expr_z3
        symVar=expr_z3.decl().name()

        symVar=rename_var(symVar)
    
        if z3.is_int(expr_z3):  symType=Sort.Int
        elif z3.is_fp(expr_z3):
            if expr_z3.sort()==z3.Float64():
                symType=Sort.Float64
            elif expr_z3.sort()==z3.Float32():
                symType=Sort.Float32
            else:
                raise NotImplementedError("Unexpected sort.", expr_z3.sort())
        elif z3.is_real(expr_z3):
            symType=Sort.Float
            warnings.warn( "****WARNING****: Real variable '%s' treated as floating point" %symVar)
        else:
            raise NotImplementedError("Unexpected type for %s" %symbolName)
        if (symVar in symbolTable.keys()):
            assert symType==symbolTable[symVar]
        else:
            symbolTable[symVar]=symType

        if expr_z3.sort()==z3.Float32():
            symVar="TR32(%s)"  %symVar # do the same ting for verify !!!!!!!!
        

        return symVar
        
    ###Leaf: val
    if _is_value(expr_z3):
        if DEBUG: print "-- Branch _is_value" 
        if z3.is_fp(expr_z3) or z3.is_real(expr_z3):
            if DEBUG: print "---- Sub-Branch FP or Real" 
            if isinstance(expr_z3,z3.FPNumRef):
                if DEBUG: print "------- Sub-Sub-Branch _is_FPNumRef"
                try:
                    str_ret=str(sympy.Float(str(expr_z3),17))

                except ValueError:
                    if expr_z3.isInf() and expr_z3.decl().kind()== z3.Z3_OP_FPA_PLUS_INF:
                        str_ret="INFINITY"
                    elif expr_z3.isInf() and expr_z3.decl().kind()== z3.Z3_OP_FPA_MINUS_INF:
                        str_ret="- INFINITY"
                    elif expr_z3.isNaN():
                        str_ret="NAN"
                    else:
                        offset=127 if expr_z3.sort()==z3.Float32() else 1023
                        #Z3 new version needs the offset to be taken into consideration
                        expr_z3_exponent=expr_z3.exponent_as_long()-offset 

                        str_ret= str(sympy.Float((-1)**float(expr_z3.sign()) * float(str(expr_z3.significand())) * 2**(expr_z3_exponent),17))

            else :
                if DEBUG: print "------- Sub-Sub-Branch other than FPNumRef, probably FPRef" 
                str_ret=str(sympy.Float(str((expr_z3)),17))
        elif z3.is_int(expr_z3):
            if DEBUG: print "---- Sub-Branch Integer"             
            str_ret=str(sympy.Integer(str(expr_z3)))
        elif _is_true(expr_z3):

            str_ret= "0"
        elif _is_false(expr_z3):
            str_ret= "1"
        else:
            raise NotImplementedError("[XSat: Coral Benchmarking] type not considered ")
        
        if expr_z3.sort()==z3.Float32():
            str_ret=str_ret+"f"
            
        return str_ret
    
    
    #if (expr_z3 in cache): return cache[expr_z3]

    #cache will be a set of defined IDs 
    #if (var_name(expr_z3) in cache): return cache[expr_z3]

    
    if (expr_z3.get_id() in cache): return var_name(expr_z3) 

    cache.add(expr_z3.get_id())
    #cache[expr_z3]=var_name(expr_z3)

    
    sort_z3=expr_z3.decl().kind()

    expr_type='double'
    if expr_z3.sort()==z3.FPSort(8,24): expr_type='float'

    ###
    if sort_z3==z3.Z3_OP_FPA_LE:
        if DEBUG: print "-- Branch _is_le"
        lhs=_gen(expr_z3.arg(0),symbolTable,cache,result)        
        rhs=_gen(expr_z3.arg(1),symbolTable,cache,result)
        toAppend= "double %s = DLE(%s,%s); " \
                  %( var_name(expr_z3), \
                     lhs,\
                     rhs,\
                  )
        result.append(toAppend)
        return var_name(expr_z3)

    #########!!!!!!!!!!!! need to do something
    if  sort_z3 == z3.Z3_OP_FPA_TO_FP: 
        if DEBUG: print "-- Branch _is_fpFP"
        assert expr_z3.num_args()==2
        if not (_is_RNE(expr_z3.arg(0))):
            warnings.warn( "WARNING!!! I expect the first argument of fpFP is RNE, but it is ",expr_z3.arg(0))
        
        x=_gen(expr_z3.arg(1),symbolTable,cache,result)
        if expr_z3.sort()==z3.FPSort(8,24):
            x = "TR32(%s)"  %x
        #else if expr_z3.sort()==z3.FPSort(8,24):
        #    x = "TR(%s)"  %x        

        toAppend= "%s %s = %s; " \
                  %( expr_type, var_name(expr_z3), \
                     x,\
                  )
        result.append(toAppend)
        return var_name(expr_z3)

    
    if sort_z3==z3.Z3_OP_FPA_LT:
        if DEBUG: print "-- Branch _is_lt"
        lhs=_gen(expr_z3.arg(0),symbolTable,cache,result)        
        rhs=_gen(expr_z3.arg(1),symbolTable,cache,result)
        toAppend= "double %s = DLT(%s,%s);" \
                  %( var_name(expr_z3), \
                     lhs,\
                     rhs,\
                  )
        result.append(toAppend)
        return var_name(expr_z3)

    if _is_eq(expr_z3):
        if DEBUG: print "-- Branch _is_eq"
        lhs=_gen(expr_z3.arg(0),symbolTable,cache,result)                
        rhs=_gen(expr_z3.arg(1),symbolTable,cache,result)
        toAppend= "double %s = DEQ(%s,%s);" \
                  %( var_name(expr_z3), \
                        lhs,\
                     rhs,\
                  )
        result.append(toAppend)
        return var_name(expr_z3)
    
    if _is_fpMul(expr_z3):
        if DEBUG: print "-- Branch _is_fpMul"
        if not _is_RNE(expr_z3.arg(0)):
            warnings.warn("WARNING!!! arg(0) is not RNE but is treated as RNE. arg(0) = ",expr_z3.arg(0))
        assert expr_z3.num_args()==3
        lhs=_gen(expr_z3.arg(1),symbolTable,cache,result)                
        rhs=_gen(expr_z3.arg(2),symbolTable,cache,result)
        toAppend= "%s %s = %s*%s; " \
                  %( expr_type, var_name(expr_z3), \
                        lhs,\
                     rhs,\

                  )
        result.append(toAppend)
        return var_name(expr_z3)
    
    if _is_fpDiv(expr_z3):
        if DEBUG: print "-- Branch _is_fpDiv"
        if not _is_RNE(expr_z3.arg(0)):
            warnings.warn("WARNING!!! arg(0) is not RNE but is treated as RNE. arg(0) = ",expr_z3.arg(0))
        assert expr_z3.num_args()==3
        lhs=_gen(expr_z3.arg(1),symbolTable,cache,result)                
        rhs=_gen(expr_z3.arg(2),symbolTable,cache,result)
        toAppend= "%s %s = %s/%s; " \
                  %(expr_type,  var_name(expr_z3), \
                        lhs,\
                     rhs,\
                  )
        result.append(toAppend)
        return var_name(expr_z3)
    
    if _is_fpAdd(expr_z3):
        if DEBUG: print "-- Branch _is_fpAdd"
        if not _is_RNE(expr_z3.arg(0)):
            warnings.warn("WARNING!!! arg(0) is not RNE but is treated as RNE. arg(0) = ",expr_z3.arg(0))
        assert expr_z3.num_args()==3
        lhs=_gen(expr_z3.arg(1),symbolTable,cache,result)                
        rhs=_gen(expr_z3.arg(2),symbolTable,cache,result)
        toAppend= "%s %s = %s+%s;" \
                  %( expr_type, var_name(expr_z3), \
                        lhs,\
                     rhs,\
                  )
        result.append(toAppend)
        return var_name(expr_z3)

    
    if z3.is_and(expr_z3):
        if DEBUG: print "-- Branch _is_and"                         
        ##TODO Not sure if symbolTable will be treated in a multi-threaded way
        toAppendExpr=_gen(expr_z3.arg(0),symbolTable,cache,result)
        for i in range(1, expr_z3.num_args()):
            toAppendExpr='BAND( %s,%s )' %(toAppendExpr,_gen(expr_z3.arg(i), symbolTable,cache, result))

        toAppend= "double %s = %s; " \
                  %( var_name(expr_z3), \
                     toAppendExpr,\
                  )
        result.append(toAppend)
        return var_name(expr_z3)

    if z3.is_not(expr_z3):
        if DEBUG: print "-- Branch _is_not"
        assert expr_z3.num_args()==1
        if not (expr_z3.arg(0).num_args()==2):
            warnings.warn ("WARNING!!! arg(0) is not RNE but is treated as RNE. arg(0) = ",expr_z3.arg(0))        
        op1= _gen( expr_z3.arg(0).arg(0),symbolTable,cache,result)
        op2= _gen( expr_z3.arg(0).arg(1), symbolTable,cache,result)
        if _is_ge(expr_z3.arg(0)):
            a= "DLT(%s,%s)" %(op1,op2)
        elif _is_gt(expr_z3.arg(0)):
            a= "DLE(%s,%s)" %(op1,op2)
        elif _is_le(expr_z3.arg(0)):
            a= "DGT(%s,%s)" %(op1,op2)
        elif _is_lt(expr_z3.arg(0)):
            a= "DGE(%s,%s)" %(op1,op2)
        elif _is_eq(expr_z3.arg(0)):
            a= "DNE(%s,%s)" %(op1,op2)
        elif _is_distinct(expr_z3.arg(0)):
            a= "DEQ(%s,%s)" %(op1,op2)
        else:
            raise NotImplementedError      ("Not implemented case 004 for expr_z3  =  %s. 'Not(or... )' is not handled yet" %expr_z3)
        toAppend= "%s %s = %s; " \
                  %( expr_type, var_name(expr_z3), \
                     a,\
                  )
        result.append(toAppend)
        return var_name(expr_z3)

    if _is_fpNeg(expr_z3):
        if DEBUG: print "-- Branch _is_fpNeg"        
        assert expr_z3.num_args()==1
        op1= _gen(expr_z3.arg(0),symbolTable,cache,result)
        toAppend = "%s %s =  - %s ;" \
                  %(expr_type, var_name(expr_z3), \
                     op1,\
                  )
        result.append(toAppend)
        return var_name(expr_z3)
        

    raise NotImplementedError ("Not implemented case 002 for expr_z3  =  %s, kind(%s)" %(expr_z3,expr_z3.decl().kind()))
    
def _is_fpNeg(a):
    return a.decl().kind()==z3.Z3_OP_FPA_NEG
def _is_fpDiv(a):
    return a.decl().kind()==z3.Z3_OP_FPA_DIV
def _is_fpMul(a):
    return a.decl().kind()==z3.Z3_OP_FPA_MUL
def _is_RNE(a):
    return a.decl().kind()==z3.Z3_OP_FPA_RM_NEAREST_TIES_TO_EVEN
def _is_fpAdd(a):
    return a.decl().kind()==z3.Z3_OP_FPA_ADD
def _is_lt(a):
    return a.decl().kind()==z3.Z3_OP_LT or a.decl().kind()==z3.Z3_OP_FPA_LT
def _is_le(a):
    return a.decl().kind()==z3.Z3_OP_LE or a.decl().kind()==z3.Z3_OP_FPA_LE
def _is_ge(a):
    return a.decl().kind()==z3.Z3_OP_GE or a.decl().kind()==z3.Z3_OP_FPA_GE
def _is_eq(a):
    return a.decl().kind()==z3.Z3_OP_EQ or a.decl().kind()==z3.Z3_OP_FPA_EQ
def _is_distinct(a):
    return a.decl().kind()==z3.Z3_OP_DISTINCT # no FPA_DISTINCT
def _is_gt(a):
    return a.decl().kind()==z3.Z3_OP_GT or a.decl().kind()==z3.Z3_OP_FPA_GT
def _dist_le(lhs,rhs):
    assert (isinstance(lhs, sympy.Expr) and isinstance(rhs,sympy.Expr))    
    return sympy.Piecewise( (lhs - rhs,lhs > rhs), (0,True))
def _dist_lt(lhs,rhs):
    assert (isinstance(lhs, sympy.Expr) and isinstance(rhs,sympy.Expr))    
    return _dist_le(lhs+_theta(), rhs)
def _dist_ge(lhs,rhs):
    assert (isinstance(lhs, sympy.Expr) and isinstance(rhs,sympy.Expr))
    return _dist_le(rhs,lhs)
def _dist_gt(lhs,rhs):
    assert (isinstance(lhs, sympy.Expr) and isinstance(rhs,sympy.Expr))    
    return _dist_lt(rhs,lhs)
def _is_true(a):
    return a.decl().kind()==z3.Z3_OP_TRUE
def _is_false(a):
    return a.decl().kind()==z3.Z3_OP_FALSE

def _dist_eq(lhs,rhs):
    assert (isinstance(lhs, sympy.Expr) and isinstance(rhs,sympy.Expr))    
    return sympy.Abs(lhs-rhs)
def _dist_distinct(lhs,rhs):
    assert (isinstance(lhs, sympy.Expr) and isinstance(rhs,sympy.Expr))
    return sympy.Piecewise( (_theta(),sympy.Eq(lhs,rhs)), (0,True))
    
def _is_fpFP(a):
    return a.decl().kind() == z3.Z3_OP_FPA_TO_FP
def _is_variable(a):
    return z3.is_const(a) and a.decl().kind() == z3.Z3_OP_UNINTERPRETED
def _is_value(a):
    return z3.is_const(a) and a.decl().kind() != z3.Z3_OP_UNINTERPRETED

def gen(expr_z3):

    symbolTable=collections.OrderedDict()
    cache=set()
    result=[]
    _gen(expr_z3,symbolTable,cache,result)   #########STOHERE
    if len(symbolTable)==0: return symbolTable,'int main(){return 0;}'
    x_expr=var_name(expr_z3)   #the last var
    x_body='\n  '.join(result)
    x_vars=','.join(symbolTable.keys())
    x_types='d'*(len(symbolTable))
    x_refs=','.join(map(lambda x: "&"+x, symbolTable.keys()))
    x_dim=len(symbolTable)

    return symbolTable,  _get_template() %{"x_vars":x_vars,"x_types":x_types,"x_refs":x_refs,"x_expr":x_expr,"x_dim":x_dim, "x_body":x_body}

def _print_xsatInfo():
    try:
        logo = open ('logo.txt',"r").read().strip('\n')
        print logo
    except:
        pass
    print
    print "*"*50
    print "XSat Version 04/04/2016 "
    print "Contributors: Zhoulai Fu and Zhendong Su"
    print "*"*50




if __name__ == "__main__":


    parser = argparse.ArgumentParser(prog='XSat')
    parser.add_argument('smt2_file', help='specify the smt2 file to analyze.',type=argparse.FileType('r'))
    parser.add_argument('-v', '--version', action='version', version='%(prog) version 12/18/2015')
    parser.add_argument ('--niter', help='niter in basinhopping', action='store', type=int, required=False,default=100)
    parser.add_argument ('--nStartOver', help='startOver times', action='store', type=int, required=False,default=2)
    parser.add_argument('--method', help='Local minimization procedure',  default='powell', choices=['powell', 'slsqp', 'cg',  'l-bfgs-b', 'cobyla','tnc',  'bfgs', 'nelder-mead','noop_min']
  )
    parser.add_argument ('--showTime', help='show the time-related info (default: false)', action='store_true', default=False)
    parser.add_argument ('--showResult', help='show the basinhopping output (default:false)', action='store_true',default=False)
    parser.add_argument ('--stepSize', help='parameter of basinhopping', type=float, default=10.0);
    parser.add_argument ('--stepSize_round2', help='parameter of basinhopping', type=float, default=100.0);        
    parser.add_argument ('--verify', help='verify the model', action='store_true',default=False)
    parser.add_argument ('--verify2', help='verify the model (method 2)', action='store_true',default=False)    
    parser.add_argument ('--showModel', help='show the model as a var->value mapping', action='store_true',default=False)
    parser.add_argument ('--showSymbolTable', help='show the symbol table, var->type', action='store_true',default=False)
    parser.add_argument ('--showConstraint', help='show the constraint, using the Z3 frontend', action='store_true',default=False)
    parser.add_argument ('--showVariableNumber', help='show variable number, using the Z3 frontend', action='store_true',default=False)

    parser.add_argument('--command_compilation', help='the command used to compile the generated foo.c to foo.so', default='gcc -O3 -fbracket-depth=2048 -fPIC -I /usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/include/python2.7/ %(file)s.c -dynamiclib -o %(file)s.so -L /usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/Current/lib/ -lpython2.7')
    parser.add_argument ('--startPoint', help='start point in a single dimension', action='store',type=float,default=1.0);
    parser.add_argument("--multi", help="multi-processing (default: false)",default=False,action='store_true')
    parser.add_argument("--multiMessage", help="multi-processing message",default=False,action='store_true')
    parser.add_argument("--round2", help="activate round2 when unsat (default: false)",default=False,action='store_true')
    parser.add_argument("--niter_round2", help="niter for round2",action='store',type=int,required=False,default=100)
    parser.add_argument("--suppressWarning", help="Suppress warnings",default=False,action='store_true')

    
    if len(sys.argv[1:])==0:
        _print_xsatInfo()
        parser.print_help()
        parser.exit()
    args = parser.parse_args()
    
    if args.suppressWarning:
        warnings.filterwarnings("ignore")

    try:
        expr_z3=z3.simplify(z3.parse_smt2_string(args.smt2_file.read()))
    except z3.Z3Exception:
        sys.stderr.write("[Xsat] The Z3 fornt-end crashes.\n")
    symbolTable, foo_dot_c=gen(expr_z3)
    args.smt2_file.close()

    #dump symbolTable for future verification step (in xsat.py)
    pickle.dump(symbolTable, open("build/foo.symbolTable","wb"))
    print foo_dot_c
