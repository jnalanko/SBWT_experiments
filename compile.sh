g++-9 -std=c++17 generate_queries.cpp -I SBWT/include -I SBWT/sdsl-lite/include/ -I SBWT/ -I SBWT/build/external/sdsl-lite/build/external/libdivsufsort/include/ SBWT/build/lib/libsbwt_static.a SBWT/build/lib/libsdsl.a -o generate_queries -O3
cd SeqIO
make
cd ..
