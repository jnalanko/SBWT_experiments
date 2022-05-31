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
                "metagenome": "./smalldata/3.fna"}
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


if sys.version_info < (3, 0):
    sys.stdout.write("Error: Python3 required\n")
    sys.exit(1)

def run_get_output(command):
    # Command can have pipes
    sys.stderr.write(command + "\n")
    return subprocess.run(command, shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

def run(command):
    sys.stderr.write(command + "\n")
    completed = subprocess.run(command, shell=True)
    if completed.returncode != 0:
        print("Error: nonzero return code for command: " + command)
        sys.exit(1)

def drop_path_and_extension(S):
    return os.path.splitext(os.path.split(S)[1])[0]

def drop_extension(S):
    return os.path.splitext()[0]

run("mkdir -p " + temp_dir)
run("mkdir -p " + unitig_dir)
run("mkdir -p " + index_dir)
run("mkdir -p " + query_dir)

