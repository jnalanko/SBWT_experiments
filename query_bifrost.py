from setup import *

print(datasets)  # Defined in setup.py

variants = ["plain-matrix", "rrr-matrix", "mef-matrix", "plain-split", "rrr-split","mef-split", "plain-concat", "mef-concat", "plain-subsetwt", "rrr-subsetwt"]

for D in datasets:
    f = datasets[D]

    # Positive queries
    run("/usr/bin/time --verbose ./bifrost/build/src/Bifrost query -g {} -q {} -o out.txt -e 1.0 2>&1 | tee {}".format(
        index_dir + "/" + D + ".bifrost.gfa",
        query_dir + "/" + D + ".pos.fa",
        query_dir + "/" + D + ".pos.bifrost.log",))

    # Negative queries
    run("/usr/bin/time --verbose ./bifrost/build/src/Bifrost query -g {} -q {} -o out.txt -e 1.0 2>&1 | tee {}".format(
        index_dir + "/" + D + ".bifrost.gfa",
        query_dir + "/" + D + ".neg.fa",
        query_dir + "/" + D + ".neg.bifrost.log",))

    # Streaming positive queries
    run("/usr/bin/time --verbose ./bifrost/build/src/Bifrost query -g {} -q {} -o out.txt -e 1.0 2>&1 | tee {}".format(
        index_dir + "/" + D + ".bifrost.gfa",
        query_dir + "/" + D + ".streaming.pos.fa",
        query_dir + "/" + D + ".streaming.pos.bifrost.log",))

    # Steaming negative queries
    run("/usr/bin/time --verbose ./bifrost/build/src/Bifrost query -g {} -q {} -o out.txt -e 1.0 2>&1 | tee {}".format(
        index_dir + "/" + D + ".bifrost.gfa",
        query_dir + "/" + D + ".streaming.neg.fa",
        query_dir + "/" + D + ".streaming.neg.bifrost.log",))