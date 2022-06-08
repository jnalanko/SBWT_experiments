#include <cstdlib>
#include <fstream>
#include <string>
#include <vector>
#include "cxxopts.hpp"
#include "SBWT.hh"
#include "variants.hh"
#include "throwing_streams.hh"

typedef long long LL;

using namespace std;
using namespace sbwt;

std::string generate_random_kmer(LL k) {
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

char incoming_label(sbwt::plain_matrix_sbwt_t& sbwt, int64_t column){
    if(column < sbwt.get_C_array()[0]) return '$';
    else if(column < sbwt.get_C_array()[1]) return 'A';
    else if(column < sbwt.get_C_array()[2]) return 'C';
    else if(column < sbwt.get_C_array()[3]) return 'G';
    else return 'T';
}

void sample_random_kmers(sbwt::plain_matrix_sbwt_t& sbwt, LL howmany, string outfile){
    cerr << "Building select supports" << endl;
    vector<sdsl::select_support_mcl<>> select_supports(4);
    sdsl::util::init_support(select_supports[0], &sbwt.get_subset_rank_structure().A_bits);
    sdsl::util::init_support(select_supports[1], &sbwt.get_subset_rank_structure().C_bits);
    sdsl::util::init_support(select_supports[2], &sbwt.get_subset_rank_structure().G_bits);
    sdsl::util::init_support(select_supports[3], &sbwt.get_subset_rank_structure().T_bits);

    cerr << "Sampling k-mers" << endl;
    throwing_ofstream out(outfile);
    LL k = sbwt.get_k();
    LL n_generated = 0;
    const vector<int64_t>& C = sbwt.get_C_array();
    while(true){
        vector<char> label(k);
        LL column = rand() % sbwt.number_of_subsets();
        bool has_dollar = false;
        for(LL j = 0; j < k; j++){
            char c = incoming_label(sbwt, column);
            label[k - 1 - j] = c;
            if(c == '$'){
                has_dollar = true;
                continue;
            }
            if(c == 'A')
                column = select_supports[0].select(column - C[0] + 1);
            if(c == 'C')
                column = select_supports[1].select(column - C[1] + 1);
            if(c == 'G')
                column = select_supports[2].select(column - C[2] + 1);
            if(c == 'T')
                column = select_supports[3].select(column - C[3] + 1);
        }

        if(!has_dollar){
            // Write out the label as a FASTA sequence
            out.stream << ">\n";
            for(char c : label) out.stream << c;
            out.stream << "\n";
            n_generated++;
            if(n_generated == howmany) return;
        }
    }
}

int main(int argc, char** argv) {

    cxxopts::Options options(argv[0], "Generates queries in fasta format (by default) for benchmarking");

    options.add_options()
        ("o,out-file", "Output filename.", cxxopts::value<string>())
        ("s,sample-from-source", "Sample k-mers from the gives fasta/fastq file.", cxxopts::value<string>()->default_value(""))
        ("i,index-file", "The plain-matrix SBWT index. If not given, uniform random k-mers are generated. If this is given, the -k option must be given", cxxopts::value<string>()->default_value(""))
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
    string source_file = opts["sample-from-source"].as<string>();
    LL howmany = opts["howmany"].as<LL>();
    LL k = opts["k"].as<LL>();
  
    sbwt::throwing_ofstream out(out_file, ios::binary);
    if(source_file != ""){
        if(k == -1){
            cerr << "k not given" << endl;
            return 1;
        }
        vector<string> seqs;
        sbwt::SeqIO::Reader<> reader(source_file);
        while(true){
            LL len = reader.get_next_read_to_buffer();
            if(len == 0) break;
            seqs.push_back(string(reader.read_buf));
        }
        while(howmany > 0){
            const string& seq = seqs[rand() % seqs.size()];
            if(seq.size() < k) continue; // Too short

            LL start = rand() % (seq.size() - k + 1);
            string S = seq.substr(start,k);

            bool is_good = true;
            for(char c : seq) if(c != 'A' && c != 'C' && c != 'G' && c != 'T') is_good = false;
            if(!is_good) continue; // Has a non-ACGT character -> don't take.

            out.stream << ">\n" << S << "\n";
            howmany--;
        }
    }
    else if(index_file == ""){
        if(k == -1){
            cerr << "k not given" << endl;
            return 1;
        }
        for (int i = 0; i < howmany; ++i) {
            out.stream << ">" << i << "\n";
            out.stream << generate_random_kmer(k) << '\n';
        }
    } else{
        if(k != -1){
            cerr << "If you give an index file, do not give k because the k is in the index." << endl;
            exit(1);
        }

        sbwt::throwing_ifstream in(index_file, ios::binary);
        string variant_on_disk = sbwt::load_string(in.stream); // read variant type
        if(variant_on_disk != "plain-matrix"){
            cerr << "Error input is not a plain-matrix SBWT." << endl;
            return 1;
        }
        plain_matrix_sbwt_t sbwt;
        sbwt.load(in.stream);
        sample_random_kmers(sbwt, howmany, out_file);
    }
}
