from setup import *
from collections import defaultdict

# Returns pair (time seconds, RSS bytes)
def parse_usr_bin_time(stderr_file):
    rss, time = None, None
    for line in open(stderr_file):
        if "Maximum resident set size (kbytes)" in line:
            rss = int(line.split()[-1]) * 2**10 # bytes
        if "Elapsed (wall clock) time (h:mm:ss or m:ss)" in line:
            token = line.split()[-1]
            hours, minutes, seconds = 0,0,0
            if token.count(":") == 1:
                minutes = float(token.split(":")[0])
                seconds = float(token.split(":")[1])
            elif token.count(":") == 2:
                hours = float(token.split(":")[0])
                minutes = float(token.split(":")[1])
                seconds = float(token.split(":")[2])
            else:
                print("Error parsing /usr/time/time -v")
                assert(False)
            time = hours * 60*60 + minutes * 60 + seconds
    if rss == None or time == None:
        print("Error parsing /usr/time/time -v from " + stderr_file)
        assert(False)
    return time, rss

def parse_us_per_query_sbwt(logfile):
    for line in open(logfile):
        if "us/query" in line and "excluding I/O etc" in line:
            return float(line.split(":")[-1].split()[0])

def parse_us_per_query_sshash(logfile):
    for line in open(logfile):
        if "Total query time ns/kmer without I/O:" in line:
            return float(line.split()[-1])

def parse_us_per_query_bifrost(logfile):
    for line in open(logfile):
        if "Total query time ns/kmer without I/O:" in line:
            return float(line.split()[-1])


print(datasets)  # Defined in setup.py

variants = ["plain-matrix", "rrr-matrix", "mef-matrix", "plain-split", "rrr-split","mef-split", "plain-concat", "mef-concat", "plain-subsetwt", "rrr-subsetwt"]
times = defaultdict(lambda: defaultdict(lambda: defaultdict(float))) # tool -> dataset -> pos/neg -> us/query
mems = defaultdict(lambda: defaultdict(lambda: defaultdict(float))) # tool -> dataset -> pos/neg -> us/query
streaming_times = defaultdict(lambda: defaultdict(lambda: defaultdict(float))) # tool -> dataset -> pos/neg -> us/query
streaming_mems = defaultdict(lambda: defaultdict(lambda: defaultdict(float))) # tool -> dataset -> pos/neg -> us/query

for D in datasets:

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
        mems[variant][D]["+"] = mem_bytes_pos

        times[variant][D]["-"] = time_us_neg
        mems[variant][D]["-"] = mem_bytes_neg

        streaming_times[variant][D]["+"] = time_streaming_us_pos
        streaming_mems[variant][D]["+"] = mem_streaming_bytes_pos

        streaming_times[variant][D]["-"] = time_streaming_us_neg
        streaming_mems[variant][D]["-"] = mem_streaming_bytes_neg

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
    mems["sshash"][D]["+"] = mem_bytes_pos

    times["sshash"][D]["-"] = time_us_neg
    mems["sshash"][D]["-"] = mem_bytes_neg

    streaming_times["sshash"][D]["+"] = time_streaming_us_pos
    streaming_mems["sshash"][D]["+"] = mem_streaming_bytes_pos

    streaming_times["sshash"][D]["-"] = time_streaming_us_neg
    streaming_mems["sshash"][D]["-"] = mem_streaming_bytes_neg

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
    mems["bifrost"][D]["+"] = mem_bytes_pos

    times["bifrost"][D]["-"] = time_us_neg
    mems["bifrost"][D]["-"] = mem_bytes_neg

    streaming_times["bifrost"][D]["+"] = time_streaming_us_pos
    streaming_mems["bifrost"][D]["+"] = mem_streaming_bytes_pos

    streaming_times["bifrost"][D]["-"] = time_streaming_us_neg
    streaming_mems["bifrost"][D]["-"] = mem_streaming_bytes_neg

print("")
print("Covid single")
for variant in (variants + ["sshash", "bifrost"]):
    print(variant, times[variant]["covid"]["+"], times[variant]["covid"]["-"])

print("")
print("Ecoli single")
for variant in (variants + ["sshash", "bifrost"]):
    print(variant, times[variant]["ecoli"]["+"], times[variant]["ecoli"]["-"])

print("")
print("Metagenome single")
for variant in (variants + ["sshash", "bifrost"]):
    print(variant, times[variant]["metagenome"]["+"], times[variant]["metagenome"]["-"])


print("")
print("Covid streaming")
for variant in (variants + ["sshash", "bifrost"]):
    print(variant, streaming_times[variant]["covid"]["+"], streaming_times[variant]["covid"]["-"])

print("")
print("Ecoli streaming")
for variant in (variants + ["sshash", "bifrost"]):
    print(variant, streaming_times[variant]["ecoli"]["+"], streaming_times[variant]["ecoli"]["-"])

print("")
print("Metagenome streaming")
for variant in (variants + ["sshash", "bifrost"]):
    print(variant, streaming_times[variant]["metagenome"]["+"], streaming_times[variant]["metagenome"]["-"])