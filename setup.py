import subprocess
import time
import sys
import os
import uuid
import signal
import random
from multiprocessing import Pool

if "--small" in sys.argv:
    datasets = {"covid": "./smalldata/1.fna",
                "ecoli": "./smalldata/2.fna",
                "metagenome": "./smalldata/3.fq"}
    unitig_dir = "./unitigs_small"
    index_dir = "./index_small"
    query_dir = "./query_small"
else:
    datasets = {"covid": "~/data/covid/ncbi_dataset/data/genomic.fna",
                "ecoli": "~/data/coli3682_concat.fasta",
                "metagenome": "~/data/ERR5035349.fastq"}
    unitig_dir = "./unitigs"
    index_dir = "./index"
    query_dir = "./query"

k = 31
n_threads = 8
temp_dir = "./temp"

my_env = os.environ.copy()
my_env["LD_LIBRARY_PATH"] = "cosmo/3rd_party_inst/boost/lib/:" + my_env["LD_LIBRARY_PATH"]

if sys.version_info < (3, 0):
    sys.stdout.write("Error: Python3 required\n")
    sys.exit(1)

def run_get_output(command):
    # Command can have pipes
    sys.stderr.write(command + "\n")
    return subprocess.run(command, shell=True, stdout=subprocess.PIPE, env=my_env).stdout.decode("utf-8").strip()

def run(command):
    sys.stderr.write(command + "\n")
    completed = subprocess.run(command, shell=True, env=my_env)
    if completed.returncode != 0:
        print("Error: nonzero return code for command: " + command)
        sys.exit(1)

def drop_path_and_extension(S):
    return os.path.splitext(os.path.split(S)[1])[0]

def drop_extension(S):
    return os.path.splitext()[0]

# Returns pair (time seconds, RSS bytes)
def parse_usr_bin_time(stderr_file):
    rss, time = None, None
    for line in open(stderr_file):
        if "Maximum resident set size (kbytes)" in line:
            rss = int(line.split()[-1]) * 2**10 # bytes
        if "Elapsed (wall clock) time (h:mm:ss or m:ss)" in line:
            token = line.split()[-1]
            hours, minutes, seconds = 0,0,0
            if token.count(":") == 1:
                minutes = float(token.split(":")[0])
                seconds = float(token.split(":")[1])
            elif token.count(":") == 2:
                hours = float(token.split(":")[0])
                minutes = float(token.split(":")[1])
                seconds = float(token.split(":")[2])
            else:
                print("Error parsing /usr/time/time -v")
                assert(False)
            time = hours * 60*60 + minutes * 60 + seconds
    if rss == None or time == None:
        print("Error parsing /usr/time/time -v from " + stderr_file)
        assert(False)
    return time, rss

def parse_kmer_count(logfile):
    for line in open(logfile):
        if "Build SBWT for" in line and "distinct k-mers" in line:
            return int(line.split()[-3])
    assert(False) # Should not come here

def parse_subset_count(logfile):
    for line in open(logfile):
        if "SBWT has " in line and "subsets" in line:
            return int(line.split()[-2])
    assert(False) # Should not come here

run("mkdir -p " + temp_dir)
run("mkdir -p " + unitig_dir)
run("mkdir -p " + index_dir)
run("mkdir -p " + query_dir)

