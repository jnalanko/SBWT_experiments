set -xue

#SIZE="--small"
SIZE="--large"

#python3 build_VARI.py $SIZE # requires VARI-merge and A LOT OF DISK.
python3 build_unitigs.py $SIZE # requires bcalm or cuttlefish
python3 stitch_unitigs.py $SIZE # requires ust
python3 build_sbwt.py $SIZE # requires sbwt with a modification that prints query time
python3 build_bifrost.py $SIZE # requires bifrost with a modification that prints query time
python3 build_sshash.py $SIZE # requires sshash
python3 generate_all_queries.py $SIZE # requires running compile.sh
python3 query_sbwt.py $SIZE # requires running compile.sh
python3 query_bifrost.py $SIZE # requires running compile.sh
python3 query_sshash.py $SIZE # requires running compile.sh
python3 query_vari.py
