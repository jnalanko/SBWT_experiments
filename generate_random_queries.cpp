#include <cstdlib>
#include <fstream>
#include <string>
#include <vector>
#include "cxxopts.hpp"
#include "BOSS.hh"
#include "throwing_streams.hh"

typedef long long LL;

using namespace std;

const std::string generate_random_kmer(LL k) {
    std::string s;

    for (int i = 0; i < k; ++i) {
        const int r = std::rand() % 4;

        switch (r) {
            case (0):
                s += 'A';
                break;
            case (1):
                s += 'C';
                break;
            case (2):
                s += 'G';
                break;
            case (3):
                s += 'T';
                break;
            default:
                break;
        }
    }

    return s;
}

vector<string> sample_random_kmers(const BOSS<sdsl::bit_vector>& wheelerboss, LL howmany){
    vector<string> kmers;
    for(LL i = 0; i < howmany; i++){
        LL colex = rand() % wheelerboss.number_of_nodes();
        string kmer = wheelerboss.get_node_label(colex);
        while(kmer.size() != wheelerboss.get_k()){
            // Dummy node. Try again.
            colex = rand() % wheelerboss.number_of_nodes();
            kmer = wheelerboss.get_node_label(colex);
        }
        kmers.push_back(kmer);
    }
    return kmers;
}

int main(int argc, char** argv) {

    cxxopts::Options options(argv[0], "Generates queries in fasta format (by default) for benchmarking");

    options.add_options()
        ("o,out-file", "Output filename.", cxxopts::value<string>())
        ("i,index-file", "The plain-matrix SBWT index. If this is given, the -k option must be given", cxxopts::value<string>()->default_value(""))
        ("n,howmany", "Number of k-mers to generate", cxxopts::value<LL>())
        ("k", "The k of the k-mers. Needed if dbg-file is not given.", cxxopts::value<LL>()->default_value("-1"))
        ("h,help", "Print usage")
    ;

    LL old_argc = argc; // Must store this because the parser modifies it
    auto opts = options.parse(argc, argv);

    if (old_argc == 1 || opts.count("help")){
        std::cerr << options.help() << std::endl;
        exit(1);
    }

    string out_file = opts["out-file"].as<string>();
    string index_file = opts["index-file"].as<string>();
    LL howmany = opts["howmany"].as<LL>();
    LL k = opts["k"].as<LL>();

    throwing_ofstream out(out_file);

    if(tdbg_file == ""){
        if(k == -1){
            cerr << "k not given" << endl;
            return 1;
        }
        for (int i = 0; i < howmany; ++i) {
            if(!no_headers) cout << ">" << i << "\n";
            out << generate_random_kmer(k) << '\n';
        }
    } else{
        if(k != -1){
            cerr << "If you give a .tdbg file, do not give k because the k is in the .tdbg." << endl;
            exit(1);
        }
        BOSS<sdsl::bit_vector> wheelerBOSS;
        throwing_ifstream in(tdbg_file, ios::binary);
        wheelerBOSS.load(in.stream);
        for(LL i = 0; i < howmany; i++){
            if(!no_headers) cout << ">" << i << "\n";
            LL colex = rand() % wheelerBOSS.number_of_nodes();
            string kmer = wheelerBOSS.get_node_label(colex);
            while(kmer.size() != wheelerBOSS.get_k()){
                // Dummy node. Try again.
                colex = rand() % wheelerBOSS.number_of_nodes();
                kmer = wheelerBOSS.get_node_label(colex);
            }
            out.stream << kmer << endl;
        }
    }
}
