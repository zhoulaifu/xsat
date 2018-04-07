#!/usr/bin/env python

import os,sys
import subprocess
import csv
import time
import gc
import collections
import argparse

OKGREEN = '\033[92m'
WARNING = '\033[93m'
ENDC = '\033[0m'

def okay( msg):
    return OKGREEN + msg + ENDC

def warn( msg):
    return  WARNING + msg + ENDC

parser = argparse.ArgumentParser(prog='test')
parser.add_argument('--quick', help='specify how fast you want the test be done', type=int, required=False, default = 1)
args = parser.parse_args() 
testFiles=["div2.c.30","mult1.c.30","div3.c.30","div.c.30","mult2.c.30",\
           "test_v7_r7_vr10_c1_s24535","test_v5_r10_vr5_c1_s13195", "div2.c.40","mult1.c.40","test_v7_r7_vr1_c1_s24449",\
           "div3.c.40","div.c.40","mult2.c.40","test_v7_r7_vr5_c1_s3582","test_v7_r7_vr1_c1_s22845",\
           "test_v7_r7_vr5_c1_s19694","test_v7_r7_vr5_c1_s14675","test_v7_r7_vr10_c1_s32506","test_v7_r7_vr10_c1_s10625","test_v7_r7_vr1_c1_s4574",\
           "test_v5_r10_vr5_c1_s8690","test_v5_r10_vr1_c1_s32538","test_v5_r10_vr5_c1_s13679","test_v5_r10_vr10_c1_s15708","test_v5_r10_vr10_c1_s7608",\
           "test_v5_r10_vr1_c1_s19145","test_v5_r10_vr1_c1_s13516","test_v5_r10_vr10_c1_s21502","sin2.c.10","div2.c.50",\
           "mult1.c.50","div3.c.50","mult2.c.50","div.c.50"]
expected_results = ["sat", "sat","sat","sat","sat","sat","sat","sat","sat","unsat","sat","sat","sat","sat","sat","sat","sat","sat","sat","sat","unsat","unsat","sat","unsat","unsat","sat","sat","unsat","sat","sat","sat","sat","sat","sat"]



for i,(f,expected) in enumerate (zip (testFiles,expected_results)):
    if (i+1)%args.quick!=0: continue
    fileName="Benchmarks/"+f+".smt2"
    print ("(%s)") %(i+1), "Working on", fileName
    COMMAND0='make -j IN=%s' %fileName 
    print "   Compiling ..."
    subprocess.check_call(COMMAND0.split(),stdout=open(os.devnull, 'wb'))
    print "   Solving ..."

    COMMAND='python xsat.py --bench'
    satisfiability=subprocess.check_output(COMMAND.split()).rstrip()
    print "   ==> "+ satisfiability, okay("[Expected]") if satisfiability==expected else warn("[Unexpected]")
