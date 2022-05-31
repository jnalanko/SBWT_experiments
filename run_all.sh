set -xue

python3 build_unitigs.py --small # requires bcalm and cuttlefish
python3 stitch_unitigs.py --small # requires ust
python3 build_sbwt.py --small # requires sbwt
python3 build_sshash.py --small # requires sshash
python3 generate_all_queries.py --small # requires running compile.sh
