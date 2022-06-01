from setup import *

print(datasets) # Defined in setup.py

variants = ["rrr-matrix", "mef-matrix", "plain-split", "rrr-split", "mef-split", "plain-concat", "mef-concat", "plain-subsetwt", "rrr-subsetwt"]

for D in datasets:
    f = datasets[D]
    logfile = index_dir + "/" + D + ".plain-matrix.sbwt.log"
    run("/usr/bin/time --verbose ./SBWT/build/bin/sbwt build -i {} -o {} -k {} --add-reverse-complements -t {} -m {} --temp-dir {}  2>&1 | tee {}".format(
          f, 
          index_dir + "/" + D + ".plain-matrix.sbwt", 
          k, 
          n_threads, 
          32, # 32GB 
          temp_dir, 
          logfile))

    # Build variants
    for variant in variants:
        logfile = index_dir + "/" + D + "." + variant + ".log"
        run("/usr/bin/time --verbose ./SBWT/build/bin/sbwt build-variant -i {} -o {} --variant {} 2>&1 | tee {}".format(
              index_dir + "/" + D + ".plain-matrix.sbwt", 
              index_dir + "/" + D + "." + variant + ".sbwt", 
              variant,
              logfile))

