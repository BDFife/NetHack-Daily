#!/usr/bin/python3

import json
from build_post import build_page

with open('index.json') as index_file:
    blog_index = json.load(index_file)

for move in blog_index:

    post = "Turn %s\n"% move['turn']
    post += "#published %s\n"% move['date']
    post += build_page(move['turn'])

    with open('%s.post'% move['turn'],
              mode='w', 
              encoding='utf-8') as blog_file:
        blog_file.write(post)

