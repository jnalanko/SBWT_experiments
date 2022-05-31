from setup import *
import sys

if "--small" in sys.argv:
    n_single_queries = 10
else:
    n_single_queries = 10**6

if "--small" in sys.argv:
    n_streaming_queries = 10
    streaming_length = 40
else:
    n_streaming_queries = 10**6 // 500
    streaming_length = 500

for D in datasets:

    # Positive single k-mer queries
    run("./generate_queries -i {} -o {} -n {}".format(
          index_dir + "/" + D + ".plain-matrix.sbwt",
          query_dir + "/" + D + ".pos.fna",
          n_single_queries))

    # Negative single k-mer queries (uniformly random k-mers)
    run("./generate_queries -o {} -n {} -k {}".format(
          query_dir + "/" + D + ".neg.fna",
          n_single_queries,
          k))

    # Positive long queries (for streaming)
    run("./generate_queries -s {} -o {} -n {} -k {}".format(
          datasets[D],
          query_dir + "/" + D + ".streaming.pos.fna",
          n_streaming_queries,
          streaming_length))

    # Negative long queries (uniformly random k-mers for large k)
    run("./generate_queries -o {} -n {} -k {}".format(
          query_dir + "/" + D + ".streaming.neg.fna",
          n_streaming_queries,
          streaming_length))
