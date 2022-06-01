from setup import *

print(datasets)  # Defined in setup.py

variants = ["plain-matrix", "rrr-matrix", "mef-matrix", "plain-split", "rrr-split","mef-split", "plain-concat", "mef-concat", "plain-subsetwt", "rrr-subsetwt"]

for D in datasets:
    f = datasets[D]

    # Positive queries
    run("/usr/bin/time --verbose ./sshash/build/query {} {} 2>&1 | tee {}".format(
        index_dir + "/" + D + ".sshash",
        query_dir + "/" + D + ".pos.fa",
        query_dir + "/" + D + ".pos.sshash.log",))

    # Negative queries
    run("/usr/bin/time --verbose ./sshash/build/query {} {} 2>&1 | tee {}".format(
        index_dir + "/" + D + ".sshash",
        query_dir + "/" + D + ".neg.fa",
        query_dir + "/" + D + ".neg.sshash.log",))

    # Streaming positive queries
    run("/usr/bin/time --verbose ./sshash/build/query {} {} 2>&1 | tee {}".format(
        index_dir + "/" + D + ".sshash",
        query_dir + "/" + D + ".streaming.pos.fa",
        query_dir + "/" + D + ".streaming.pos.sshash.log",))

    # Steaming negative queries
    run("/usr/bin/time --verbose ./sshash/build/query {} {} 2>&1 | tee {}".format(
        index_dir + "/" + D + ".sshash",
        query_dir + "/" + D + ".streaming.neg.fa",
        query_dir + "/" + D + ".streaming.neg.sshash.log",))