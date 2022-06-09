from setup import *
from collections import defaultdict

def parse_us_per_query_sbwt(logfile):
    for line in open(logfile):
        if "us/query" in line and "excluding I/O etc" in line:
            return float(line.split(":")[-1].split()[0])

def parse_us_per_query_sshash(logfile):
    for line in open(logfile):
        if "Total query time us/kmer without I/O:" in line:
            return float(line.split()[-1])

def parse_us_per_query_bifrost(logfile):
    for line in open(logfile):
        if "Total query time us/kmer without I/O:" in line:
            return float(line.split()[-1])


print(datasets)  # Defined in setup.py

variants = ["plain-matrix", "rrr-matrix", "mef-matrix", "plain-split", "rrr-split","mef-split", "plain-concat", "mef-concat", "plain-subsetwt", "rrr-subsetwt"]
times = defaultdict(lambda: defaultdict(lambda: defaultdict(float))) # tool -> dataset -> pos/neg -> us/query
mems = defaultdict(lambda: defaultdict(lambda: defaultdict(float))) # tool -> dataset -> pos/neg -> mem
streaming_times = defaultdict(lambda: defaultdict(lambda: defaultdict(float))) # tool -> dataset -> pos/neg -> us/query
streaming_mems = defaultdict(lambda: defaultdict(lambda: defaultdict(float))) # tool -> dataset -> pos/neg -> mem

for D in datasets:

    kmers = parse_kmer_count(index_dir + "/" + D + ".plain-matrix-no-rc.log") # Counting k-mers, not k-molecules
    streaming_overhead = parse_subset_count(index_dir + "/" + D + ".plain-matrix.log")
    # SBWT variants
    for variant in variants:
        f = datasets[D]

        pos_file = query_dir + "/" + D + ".pos." + variant + ".sbwt.log"
        neg_file = query_dir + "/" + D + ".neg." + variant + ".sbwt.log"
        streaming_pos_file = query_dir + "/" + D + ".streaming.pos." + variant + ".sbwt.log"
        streaming_neg_file = query_dir + "/" + D + ".streaming.neg." + variant + ".sbwt.log"

        total_time_pos, mem_bytes_pos = parse_usr_bin_time(pos_file)
        time_us_pos = parse_us_per_query_sbwt(pos_file) 

        total_time_neg, mem_bytes_neg = parse_usr_bin_time(neg_file)
        time_us_neg = parse_us_per_query_sbwt(neg_file) 
        
        total_streaming_time_pos, mem_streaming_bytes_pos = parse_usr_bin_time(streaming_pos_file)
        time_streaming_us_pos = parse_us_per_query_sbwt(streaming_pos_file) 

        total_streaming_time_neg, mem_streaming_bytes_neg = parse_usr_bin_time(streaming_neg_file)
        time_streaming_us_neg = parse_us_per_query_sbwt(streaming_neg_file) 
        
        times[variant][D]["+"] = time_us_pos
        mems[variant][D]["+"] = (float(mem_bytes_pos)*8 - streaming_overhead) / kmers # Subtract the streaming overhead becaues it's not need for single queries

        times[variant][D]["-"] = time_us_neg
        mems[variant][D]["-"] = (float(mem_bytes_neg)*8 - streaming_overhead) / kmers # Subtract the streaming overhead becaues it's not need for single queries

        streaming_times[variant][D]["+"] = time_streaming_us_pos
        streaming_mems[variant][D]["+"] = float(mem_streaming_bytes_pos)*8 / kmers

        streaming_times[variant][D]["-"] = time_streaming_us_neg
        streaming_mems[variant][D]["-"] = float(mem_streaming_bytes_neg)*8 / kmers

    # sshash

    pos_file = query_dir + "/" + D + ".pos.sshash.log"
    neg_file = query_dir + "/" + D + ".neg.sshash.log"
    streaming_pos_file = query_dir + "/" + D + ".streaming.pos.sshash.log"
    streaming_neg_file = query_dir + "/" + D + ".streaming.neg.sshash.log"

    total_time_pos, mem_bytes_pos = parse_usr_bin_time(pos_file)
    time_us_pos = parse_us_per_query_sshash(pos_file) 

    total_time_neg, mem_bytes_neg = parse_usr_bin_time(neg_file)
    time_us_neg = parse_us_per_query_sshash(neg_file) 
    
    total_streaming_time_pos, mem_streaming_bytes_pos = parse_usr_bin_time(streaming_pos_file)
    time_streaming_us_pos = parse_us_per_query_sshash(streaming_pos_file) 

    total_streaming_time_neg, mem_streaming_bytes_neg = parse_usr_bin_time(streaming_neg_file)
    time_streaming_us_neg = parse_us_per_query_sshash(streaming_neg_file) 

    times["sshash"][D]["+"] = time_us_pos
    mems["sshash"][D]["+"] = float(mem_bytes_pos) * 8 / kmers

    times["sshash"][D]["-"] = time_us_neg
    mems["sshash"][D]["-"] = float(mem_bytes_neg) * 8 / kmers

    streaming_times["sshash"][D]["+"] = time_streaming_us_pos
    streaming_mems["sshash"][D]["+"] = float(mem_streaming_bytes_pos) * 8 / kmers

    streaming_times["sshash"][D]["-"] = time_streaming_us_neg
    streaming_mems["sshash"][D]["-"] = float(mem_streaming_bytes_neg) * 8 / kmers

    # bifrost

    pos_file = query_dir + "/" + D + ".pos.bifrost.log"
    neg_file = query_dir + "/" + D + ".neg.bifrost.log"
    streaming_pos_file = query_dir + "/" + D + ".streaming.pos.bifrost.log"
    streaming_neg_file = query_dir + "/" + D + ".streaming.neg.bifrost.log"

    total_time_pos, mem_bytes_pos = parse_usr_bin_time(pos_file)
    time_us_pos = parse_us_per_query_sshash(pos_file) 

    total_time_neg, mem_bytes_neg = parse_usr_bin_time(neg_file)
    time_us_neg = parse_us_per_query_sshash(neg_file) 
    
    total_streaming_time_pos, mem_streaming_bytes_pos = parse_usr_bin_time(streaming_pos_file)
    time_streaming_us_pos = parse_us_per_query_sshash(streaming_pos_file) 

    total_streaming_time_neg, mem_streaming_bytes_neg = parse_usr_bin_time(streaming_neg_file)
    time_streaming_us_neg = parse_us_per_query_sshash(streaming_neg_file) 

    times["bifrost"][D]["+"] = time_us_pos
    mems["bifrost"][D]["+"] = float(mem_bytes_pos) * 8 / kmers

    times["bifrost"][D]["-"] = time_us_neg
    mems["bifrost"][D]["-"] = float(mem_bytes_neg) * 8 / kmers

    streaming_times["bifrost"][D]["+"] = time_streaming_us_pos
    streaming_mems["bifrost"][D]["+"] = float(mem_streaming_bytes_pos) * 8 / kmers

    streaming_times["bifrost"][D]["-"] = time_streaming_us_neg
    streaming_mems["bifrost"][D]["-"] = float(mem_streaming_bytes_neg) * 8 / kmers

print("")
print("Covid")
for variant in (variants + ["sshash", "bifrost"]):
    print(variant + " &", 
          "{:.2f} &".format(times[variant]["covid"]["+"]),
          "{:.2f} &".format(times[variant]["covid"]["-"]),
          "{:.2f} &".format(mems[variant]["covid"]["+"]),
          "{:.2f} &".format(streaming_times[variant]["covid"]["+"]),
          "{:.2f} &".format(streaming_times[variant]["covid"]["-"]),
          "{:.2f} \\\\".format(streaming_mems[variant]["covid"]["+"]))

print("")
print("Ecoli")
for variant in (variants + ["sshash", "bifrost"]):
    print(variant + " &", 
          "{:.2f} &".format(times[variant]["ecoli"]["+"]),
          "{:.2f} &".format(times[variant]["ecoli"]["-"]),
          "{:.2f} &".format(mems[variant]["ecoli"]["+"]),
          "{:.2f} &".format(streaming_times[variant]["ecoli"]["+"]),
          "{:.2f} &".format(streaming_times[variant]["ecoli"]["-"]),
          "{:.2f} \\\\".format(streaming_mems[variant]["ecoli"]["+"]))
print("")
print("Metagenome")
for variant in (variants + ["sshash", "bifrost"]):
    print(variant + " &", 
          "{:.2f} &".format(times[variant]["metagenome"]["+"]),
          "{:.2f} &".format(times[variant]["metagenome"]["-"]),
          "{:.2f} &".format(mems[variant]["metagenome"]["+"]),
          "{:.2f} &".format(streaming_times[variant]["metagenome"]["+"]),
          "{:.2f} &".format(streaming_times[variant]["metagenome"]["-"]),
          "{:.2f} \\\\".format(streaming_mems[variant]["metagenome"]["+"]))
