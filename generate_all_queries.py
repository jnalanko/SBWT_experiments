from setup import *
import sys

if "--small" in sys.argv:
    n_queries = 10
else:
    n_queries = 10**6

for D in datasets:
    f = datasets[D]

    # Positive queries
    run("./generate_random_queries -i {} -o {} -n {}".format(
          index_dir + "/" + D + ".plain-matrix.sbwt",
          query_dir + "/" + D + ".pos.fna",
          n_queries))

    # Negative queries
    run("./generate_random_queries -o {} -n {} -k {}".format(
          query_dir + "/" + D + ".neg.fna",
          n_queries,
          k))

