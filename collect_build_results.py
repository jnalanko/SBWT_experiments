from setup import *
from collections import defaultdict

variants = ["plain-matrix", "rrr-matrix", "mef-matrix", "plain-split", "rrr-split","mef-split", "plain-concat", "mef-concat", "plain-subsetwt", "rrr-subsetwt"]

times = defaultdict(lambda: defaultdict(float)) # tool -> dataset -> time in seconds
mems = defaultdict(lambda: defaultdict(int)) # tool -> dataset -> peak RSS in bytes
sizes = defaultdict(lambda: defaultdict(int)) # tool -> dataset -> final size on disk in bytes

# Get times and memories from /usr/bin/time --verbose output
for D in datasets:
    # SBWT variants
    for variant in variants:
        logfile = index_dir + "/" + D + "." + variant + ".log"
        time, rss = parse_usr_bin_time(logfile)

        if variant != "plain-matrix":
            # Since we are building through plain matrix, we need to include the time and memory for that
            time_plain, rss_plain = parse_usr_bin_time(index_dir + "/" + D + ".plain-matrix.log")
            rss = max(rss, rss_plain)
            time += time_plain 

        times[variant][D] = time
        mems[variant][D] = rss

    # sshash
    logfile = index_dir + "/" + D + ".sshash.log"
    time, rss = parse_usr_bin_time(logfile)
    logfile = unitig_dir + "/" + D + ".bcalm.log"
    time_bc, rss_bc = parse_usr_bin_time(logfile) # Including BCALM time
    logfile = unitig_dir + "/" + D + ".ust.log"
    time_ust, rss_ust = parse_usr_bin_time(logfile) # Including UST time
    times["sshash"][D] = time + time_bc + time_ust
    mems["sshash"][D] = max(rss, rss_bc, time_ust)

    # bifrost
    logfile = index_dir + "/" + D + ".bifrost.log"
    time, rss = parse_usr_bin_time(logfile)
    times["bifrost"][D] = time
    mems["bifrost"][D] = rss

# Get sizes on disk
ls = run_get_output("ls -l index")
for line in ls.split("\n")[1:]:

    if line.split()[-1].split(".")[-1] in ["sbwt", "sshash", "gfa"]:
        size = line.split()[4]
        filename = line.split()[-1]
        dataset = filename.split(".")[0]
        method = filename.split(".")[1]
        sizes[method][dataset] = size


print("")
print("Covid")
for variant in (variants + ["sshash", "bifrost"]):
    print(variant, times[variant]["covid"], mems[variant]["covid"], sizes[variant]["covid"])

print("")
print("Ecoli")
for variant in (variants + ["sshash", "bifrost"]):
    print(variant, times[variant]["ecoli"], mems[variant]["ecoli"], sizes[variant]["ecoli"])

print("")
print("Metagenome")
for variant in (variants + ["sshash", "bifrost"]):
    print(variant, times[variant]["metagenome"], mems[variant]["metagenome"], sizes[variant]["metagenome"])


        

