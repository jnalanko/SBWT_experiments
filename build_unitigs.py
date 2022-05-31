from setup import *

print(datasets) # Defined in setup.py

if ".json" in run_get_output("ls " + unitig_dir):
    run("rm {}/*.json".format(unitig_dir)) # Need to remove these or cuttlefish wont build the graph

for D in datasets:
    f = datasets[D]
    run("./cuttlefish/build/src/cuttlefish build -s {} -k {} -t {} -o {} -w {}".format(
        f, k, n_threads, unitig_dir + "/" + D, tempdir))


