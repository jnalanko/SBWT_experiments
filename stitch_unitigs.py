from setup import *

# Remember to set `ulimit -n 2048` or else Cuttlefish will crash.

print(datasets) # Defined in setup.py

for D in datasets:
    f = datasets[D]
    logfile = unitig_dir + "/" + D + ".ust.log"
    run("/usr/bin/time --verbose UST/ust -k {} -i {} 2>&1 | tee {}".format(
         k, unitig_dir + "/" + D + ".unitigs.fa", logfile))
    run("mv " + D + ".unitigs.fa.ust.fa* " + unitig_dir)

