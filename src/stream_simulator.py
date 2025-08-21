import json
import time
import sys

with open('data/sample_data.json','r')as f:
    data = json.load(f)
    for entry in data:
        print(json.dumps(entry))

        sys.stdout.flush()
        time.sleep(1)
