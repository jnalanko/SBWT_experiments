from setup import *

print(datasets) # Defined in setup.py

variants = ["rrr-matrix", "mef-matrix", "plain-split", "rrr-split", "mef-split", "plain-concat", "mef-concat", "plain-subsetwt", "rrr-subsetwt"]

for D in datasets:
    f = datasets[D]

    if D == "covid": mem_gigas = 5
    if D == "ecoli": mem_gigas = 5
    if D == "metagenome": mem_gigas = 9

    # With rc
    run("/usr/bin/time --verbose ./SBWT/build/bin/sbwt build -i {} -o {} -k {} --add-reverse-complements -t {} -m {} --temp-dir {}  2>&1 | tee {}".format(
          f, 
          index_dir + "/" + D + ".plain-matrix.sbwt", 
          k, 
          n_threads, 
          mem_gigas,
          temp_dir,
          index_dir + "/" + D + ".plain-matrix.log"))
    # With rc
    run("/usr/bin/time --verbose ./SBWT/build/bin/sbwt build -i {} -o {} -k {} -t {} -m {} --temp-dir {}  2>&1 | tee {}".format(
          f, 
          index_dir + "/" + D + ".plain-matrix-no-rc.sbwt", 
          k, 
          n_threads, 
          mem_gigas,
          temp_dir,
          index_dir + "/" + D + ".plain-matrix-no-rc.log"))


    # Build variants
    for variant in variants:

        # rc
        run("/usr/bin/time --verbose ./SBWT/build/bin/sbwt build-variant -i {} -o {} --variant {} 2>&1 | tee {}".format(
              index_dir + "/" + D + ".plain-matrix.sbwt", 
              index_dir + "/" + D + "." + variant + ".sbwt", 
              variant,
              index_dir + "/" + D + "." + variant + ".log"))

        # no rc
        run("/usr/bin/time --verbose ./SBWT/build/bin/sbwt build-variant -i {} -o {} --variant {} 2>&1 | tee {}".format(
              index_dir + "/" + D + ".plain-matrix-no-rc.sbwt", 
              index_dir + "/" + D + "." + variant + "-no-rc.sbwt", 
              variant,
              index_dir + "/" + D + "." + variant + "-no-rc.log"))
