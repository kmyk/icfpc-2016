```
./a.py snapshot | jq -r '.problems[] | ( .problem_id | tostring ) + " " + .problem_spec_hash' | while read id hash ; do cat ../cache/blob/$hash | ../visualizer/a.py -p > ../data/problem-$id.input.png ; done
```
