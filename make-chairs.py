#!/usr/bin/env python

import json

chairs = []
with open('chairs.txt') as f:
    for line in f:
        id, chair, email = line.strip().split('\t')
        chairs.append({
            'id': int(id.strip()),
            'chair': chair.strip(),
            'email': email.strip()
        })

with open('chairs.json', 'w') as f:
    json.dump(chairs, f, indent=True, separators=(',', ': '))
