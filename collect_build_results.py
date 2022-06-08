from setup import *
from collections import defaultdict

def parse_kmer_count(logfile):
    for line in open(logfile):
        if "Build SBWT for" in line and "distinct k-mers" in line:
            return int(line.split()[-3])
    assert(False) # Should not come here

def parse_subset_count(logfile):
    for line in open(logfile):
        if "SBWT has " in line and "subsets" in line:
            return int(line.split()[-2])
    assert(False) # Should not come here

def print_table(dataset):
    streaming_overhead_rc = parse_subset_count(index_dir + "/" + dataset + ".plain-matrix.log")
    streaming_overhead_no_rc = parse_subset_count(index_dir + "/" + dataset + ".plain-matrix-no-rc.log")
    kmers = parse_kmer_count(index_dir + "/" + dataset + ".plain-matrix-no-rc.log")

    for variant in variants:
        size_rc = (sizes[variant][dataset]*8 - streaming_overhead_rc) / kmers
        size_no_rc = (sizes[variant + "-no-rc"][dataset]*8 - streaming_overhead_no_rc) / kmers
        print("& " + variant, 
            "& {} | {}".format(int(times[variant][dataset]), int(times[variant + "-no-rc"][dataset])),  # Seconds
            "& {:.3g} | {:.3g}".format(mems[variant][dataset] / 2**30, mems[variant + "-no-rc"][dataset] / 2**30), # GB
            "& {:.3g} | {:.3g}".format(size_rc, size_no_rc)) # bits / kmer

    for variant in ["sshash", "bifrost"]: 
        print("& " + variant, 
            "& {} ".format(int(times[variant][dataset])),  # Seconds
            "& {:.3g} ".format(mems[variant][dataset] / 2**30), # GB
            "& {:.3g} ".format(sizes[variant][dataset]*8 / kmers)) # bits / kmer

variants = ["plain-matrix", "rrr-matrix", "mef-matrix", "plain-split", "rrr-split","mef-split", "plain-concat", "mef-concat", "plain-subsetwt", "rrr-subsetwt"]
variants_both = variants + [x + "-no-rc" for x in variants] # Add no-reverse-complement versions

times = defaultdict(lambda: defaultdict(float)) # tool -> dataset -> time in seconds
mems = defaultdict(lambda: defaultdict(int)) # tool -> dataset -> peak RSS in bytes
sizes = defaultdict(lambda: defaultdict(int)) # tool -> dataset -> final size on disk in bytes

# Get times and memories from /usr/bin/time --verbose output
for D in datasets:
    # SBWT variants
    for variant in variants_both:
        logfile = index_dir + "/" + D + "." + variant + ".log"
        time, rss = parse_usr_bin_time(logfile)

        if "plain-matrix" not in variant:
            # Since we are building through plain matrix, we need to include the time and memory for that
            if variant[-5:] == "no-rc":
                time_plain, rss_plain = parse_usr_bin_time(index_dir + "/" + D + ".plain-matrix-no-rc.log")
            else:
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
        sizes[method][dataset] = int(size)


print("")
print("Covid")
print_table("covid")

print("")
print("Ecoli")
print_table("ecoli")


print("")
print("metagenome")
print_table("metagenome")



        

