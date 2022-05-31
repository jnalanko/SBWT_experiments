set -xue

python3 build_unitigs.py --small
python3 stitch_unitigs.py --small
python3 build_sbwt.py --small
python3 build_sshash.py --small
python3 generate_all_queries.py --small
