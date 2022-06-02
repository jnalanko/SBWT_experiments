from setup import *

for D in datasets:
    f = datasets[D]

    # Positive queries
    run("/usr/bin/time --verbose ./cosmo/cosmo-benchmark {} {} 2>&1 | tee {}".format(
        index_dir + "/" + D + ".vari_list.dbg",
        query_dir + "/" + D + ".pos.fa",
        query_dir + "/" + D + ".pos.vari.log",))

    # Negative queries
    run("/usr/bin/time --verbose ./cosmo/cosmo-benchmark {} {} 2>&1 | tee {}".format(
        index_dir + "/" + D + ".vari_list.dbg",
        query_dir + "/" + D + ".neg.fa",
        query_dir + "/" + D + ".neg.vari.log",))

    # Streaming positive queries
    run("/usr/bin/time --verbose ./cosmo/cosmo-benchmark {} {} 2>&1 | tee {}".format(
        index_dir + "/" + D + ".vari_list.dbg",
        query_dir + "/" + D + ".streaming.pos.fa",
        query_dir + "/" + D + ".streaming.pos.vari.log",))

    # Steaming negative queries
    run("/usr/bin/time --verbose ./cosmo/cosmo-benchmark {} {} 2>&1 | tee {}".format(
        index_dir + "/" + D + ".vari_list.dbg",
        query_dir + "/" + D + ".streaming.neg.fa",
        query_dir + "/" + D + ".streaming.neg.vari.log",))
