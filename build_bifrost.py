from setup import *

for D in datasets:
    f = datasets[D]
    logfile = index_dir + "/" + D + ".bifrost.log"
    run("/usr/bin/time --verbose ./bifrost/build/src/Bifrost build -r {} -o {} -t {} -k {} -y 2>&1 | tee {}".format(
        f, 
        index_dir + "/" + D + ".bifrost", # Bifrost will append .gfa
        n_threads,
        k,
        logfile
    ))