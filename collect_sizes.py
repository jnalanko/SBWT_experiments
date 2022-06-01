from setup import *

variants = ["rrr-matrix", "mef-matrix", "plain-split", "rrr-split", "mef-split", "plain-concat", "mef-concat", "plain-subsetwt", "rrr-subsetwt"]

ls = run_get_output("ls -l index")

for line in ls.split("\n")[1:]:
    if line.split()[-1].split(".")[-1] != "log":
        size = line.split()[4]
        filename = line.split()[-1]
        dataset = filename.split(".")[0]
        method = filename.split(".")[1]
        print(size,dataset,method)
        
        

        

