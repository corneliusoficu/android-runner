#!/bin/bash
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 NUM_RUNS"
  exit 1
fi
source ../venv/bin/activate

echo "Executing experiment for $1 times"
cd ../

for i in `seq $1`; do
  echo "Executing experiment: $i"
  python3 android-runner/ android-runner/examples/perfume_power/config_web.json;
done

