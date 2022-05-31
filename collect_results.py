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

def parse_us_per_query(logfile):
    for line in open(logfile):
        if "us/query" in line and "excluding I/O etc" in line:
            return float(line.split(":")[-1].split()[0])

print(datasets)  # Defined in setup.py

variants = ["plain-matrix", "rrr-matrix", "mef-matrix", "plain-split", "rrr-split","mef-split", "plain-concat", "mef-concat", "plain-subsetwt", "rrr-subsetwt"]
times = defaultdict(lambda: defaultdict(lambda: defaultdict(float))) # tool -> dataset -> pos/neg -> us/query
mems = defaultdict(lambda: defaultdict(lambda: defaultdict(float))) # tool -> dataset -> pos/neg -> us/query


for variant in variants:
    for D in datasets:
        f = datasets[D]

        pos_file = query_dir + "/" + D + ".pos." + variant + ".sbwt.log"
        neg_file = query_dir + "/" + D + ".pos." + variant + ".sbwt.log"

        total_time_pos, mem_bytes_pos = parse_usr_bin_time(pos_file)
        time_us_pos = parse_us_per_query(pos_file) 

        total_time_neg, mem_bytes_neg = parse_usr_bin_time(neg_file)
        time_us_neg = parse_us_per_query(neg_file) 

        times[variant][D]["+"] = time_us_pos
        mems[variant][D]["+"] = mem_bytes_pos

        times[variant][D]["-"] = time_us_neg
        mems[variant][D]["-"] = mem_bytes_neg

print("")
print("Covid")
for variant in variants:
    print(variant, times[variant]["covid"]["+"], times[variant]["covid"]["-"])

print("")
print("Ecoli")
for variant in variants:
    print(variant, times[variant]["ecoli"]["+"], times[variant]["ecoli"]["-"])

print("")
print("Metagenome")
for variant in variants:
    print(variant, times[variant]["metagenome"]["+"], times[variant]["metagenome"]["-"])