from setup import *

print(datasets) # Defined in setup.py

minimizer_len = 13 # From the example in the README

for D in datasets:
    f = datasets[D]
    run("./sshash/build/build {} {} {} -o {}".format(
        unitig_dir + "/" + D + ".unitigs.fa", k, minimizer_len, index_dir + "/" + D + ".sshash"))


