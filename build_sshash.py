from setup import *

print(datasets) # Defined in setup.py

minimizer_len = 16

for D in datasets:
    f = datasets[D]
    logfile = index_dir + "/" + D + ".sshash.log"
    run("/usr/bin/time --verbose ./sshash/build/build {} {} {} -o {} 2>&1 | tee {}".format(
        unitig_dir + "/" + D + ".unitigs.fa.ust.fa", k, minimizer_len, index_dir + "/" + D + ".sshash", logfile))


