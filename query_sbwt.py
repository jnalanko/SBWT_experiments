from setup import *

print(datasets)  # Defined in setup.py

variants = ["plain-matrix", "rrr-matrix", "mef-matrix", "plain-split", "rrr-split","mef-split", "plain-concat", "mef-concat", "plain-subsetwt", "rrr-subsetwt"]

for D in datasets:
    f = datasets[D]

    for variant in variants:
        # Positive queries
        run("/usr/bin/time --verbose ./SBWT/build/bin/sbwt search -o {} -i {} -q {} 2>&1 | tee {}".format(
            query_dir + "/" + D + ".pos." + variant + ".sbwt.out",
            index_dir + "/" + D + "." + variant + ".sbwt",
            query_dir + "/" + D + ".pos.fa",
            query_dir + "/" + D + ".pos." + variant + ".sbwt.log",))

        # Negative queries
        run("/usr/bin/time --verbose ./SBWT/build/bin/sbwt search -o {} -i {} -q {} 2>&1 | tee {}".format(
            query_dir + "/" + D + ".neg." + variant + ".sbwt.out",
            index_dir + "/" + D + "." + variant + ".sbwt",
            query_dir + "/" + D + ".neg.fa",
            query_dir + "/" + D + ".neg." + variant + ".sbwt.log",))

        # Streaming positive queries
        run("/usr/bin/time --verbose ./SBWT/build/bin/sbwt search -o {} -i {} -q {} 2>&1 | tee {}".format(
            query_dir + "/" + D + ".streaming.pos." + variant + ".sbwt.out",
            index_dir + "/" + D + "." + variant + ".sbwt",
            query_dir + "/" + D + ".streaming.pos.fa",
            query_dir + "/" + D + ".streaming.pos." + variant + ".sbwt.log",))

        # Steaming negative queries
        run("/usr/bin/time --verbose ./SBWT/build/bin/sbwt search -o {} -i {} -q {} 2>&1 | tee {}".format(
            query_dir + "/" + D + ".streaming.neg." + variant + ".sbwt.out",
            index_dir + "/" + D + "." + variant + ".sbwt",
            query_dir + "/" + D + ".streaming.neg.fa",
            query_dir + "/" + D + ".streaming.neg." + variant + ".sbwt.log",))