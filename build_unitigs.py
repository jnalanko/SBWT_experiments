from setup import *

# Remember to set `ulimit -n 2048` or else Cuttlefish will crash.

print(datasets) # Defined in setup.py

def run_cuttlefish():

    if ".json" in run_get_output("ls " + unitig_dir):
        run("rm {}/*.json".format(unitig_dir)) # Need to remove these or cuttlefish wont build the graph

    for D in datasets:
        f = datasets[D]
        logfile = unitig_dir + "/" + D + ".cuttlefish.log"
        run("./cuttlefish/build/src/cuttlefish build -s {} -k {} -t {} -o {} -w {} 2>&1 | tee {}".format(
            f, k, n_threads, unitig_dir + "/" + D, tempdir, logfile, logfile))

def run_bcalm():
    for D in datasets:
        f = datasets[D]
        logfile = unitig_dir + "/" + D + ".bcalm.log"
        run("/usr/bin/time --verbose bcalm/build/bcalm -in {} -kmer-size {} -abundance-min 1 -nb-cores {} -out {} 2>&1 | tee {}".format(
             f, k, n_threads, unitig_dir + "/" + D, logfile, logfile))

run_bcalm()

#~/bcalm/build/bcalm -in ~/DNA_datasets/Homo_sapiens.GRCh38.dna.chromosome.13.fa.gz -kmer-size 31 -abundance-min 1 -nb-cores 8
