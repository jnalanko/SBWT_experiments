from setup import *

# export LD_LIBRARY_PATH=cosmo/3rd_party_inst/boost/lib/

# ./KMC/bin/kmc -ci0 -fm -k31 test.fna test.fna temp
# ./KMC/bin/kmc_tools transform test.fna sort test.fna.sorted
# echo test.fna.sorted > vari_list.txt
# ./cosmo/cosmo-build -d vari_list.txt

for D in datasets:
    f = datasets[D]

    run("/usr/bin/time --verbose ./KMC/bin/kmc -ci0 -cs2 {} -k{} {} {} {}  2>&1 | tee {}".format(
          "-fq" if D == "metagenome" else "-fm", # Metagenome is in fastq format, others in multi-fasta
          k, 
          f,
          temp_dir + "/kmc1",
          temp_dir,
          index_dir + "/" + D + ".kmc1.log"
          ))
    run("/usr/bin/time --verbose ./KMC/bin/kmc_tools transform {} sort {} 2>&1 | tee {}".format(
          temp_dir + "/kmc1",
          temp_dir + "/kmc2",
          index_dir + "/" + D + ".kmc2.log"
          ))
    
    run("echo {} > {}".format(
        temp_dir + "/kmc2",
        temp_dir + "/vari_list.txt"
    ))

    run("/usr/bin/time --verbose ./cosmo/cosmo-build -d {} -o {} 2>&1 | tee {}".format(
        temp_dir + "/vari_list.txt",
        index_dir + "/" + D + ".", # Vari adds suffix vari_list.dbg
        index_dir + "/" + D + ".vari.log"
    ))

