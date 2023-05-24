#!/bin/bash

usage() {
    echo "Usage: $0 <version1> <version2>"
    echo "Example: $0 V24.0 V25.0RC3"
    exit 1
}

if [ $# -ne 2 ]; then
    usage
fi

VERSION1=$1
VERSION2=$2

FILENAME1=$(echo "$VERSION1" | tr '.' '-')
FILENAME2=$(echo "$VERSION2" | tr '.' '-')
COMPARE_FOLDER="compare_${FILENAME1}_${FILENAME2}"
mkdir -p "$COMPARE_FOLDER"

./nanomock_manager.sh "nanocurrency/nano:$VERSION1" --restore-ledger
sleep 5
python3 run_rpc_multicall.py -url http://localhost:45101 -v 23.3 -f "$VERSION1" > "$COMPARE_FOLDER/v1_filename1.out"
sleep 2
python3 run_rpc_multicall.py -url http://localhost:45101 -v 23.3 -f "$VERSION1-r2" > "$COMPARE_FOLDER/v1_filename2.out"

./nanomock_manager.sh "nanocurrency/nano:$VERSION2" --restore-ledger
sleep 5
python3 run_rpc_multicall.py -url http://localhost:45101 -v 23.3 -f "$VERSION2" > "$COMPARE_FOLDER/v2_filename1.out"
sleep 2
python3 run_rpc_multicall.py -url http://localhost:45101 -v 23.3 -f "$VERSION2-r2" > "$COMPARE_FOLDER/v2_filename2.out"

FILENAME_V1_1=$(tail -n 1 "$COMPARE_FOLDER/v1_filename1.out")
FILENAME_V1_2=$(tail -n 1 "$COMPARE_FOLDER/v1_filename2.out")
FILENAME_V2_1=$(tail -n 1 "$COMPARE_FOLDER/v2_filename1.out")
FILENAME_V2_2=$(tail -n 1 "$COMPARE_FOLDER/v2_filename2.out")

python3 run_deep_diff.py "$FILENAME_V1_1" "$FILENAME_V1_2" -o "$COMPARE_FOLDER/baseline_$FILENAME1.json"
python3 run_deep_diff.py "$FILENAME_V2_1" "$FILENAME_V2_2" -o "$COMPARE_FOLDER/baseline_$FILENAME2.json"
python3 run_deep_diff.py "$FILENAME_V1_1" "$FILENAME_V2_1" -o "$COMPARE_FOLDER/diff_$FILENAME1_$FILENAME2.json"

python3 run_baseline_filter.py "$COMPARE_FOLDER/baseline_$FILENAME1.json" "$COMPARE_FOLDER/diff_$FILENAME1_$FILENAME2.json" "$COMPARE_FOLDER/diff_$FILENAME1_$FILENAME2_filter_$FILENAME1.json"
python3 run_baseline_filter.py "$COMPARE_FOLDER/baseline_$FILENAME2.json" "$COMPARE_FOLDER/diff_$FILENAME1_$FILENAME2_filter_$FILENAME1.json" "$COMPARE_FOLDER/diff_$FILENAME1_$FILENAME2_filter_$FILENAME1_$FILENAME2.json"

python3 run_reformat_diff.py -i "$COMPARE_FOLDER/diff_$FILENAME1_$FILENAME2_filter_$FILENAME1_$FILENAME2.json" -o "$COMPARE_FOLDER/FINAL_inspectable_${VERSION1}_${VERSION2}.json"
