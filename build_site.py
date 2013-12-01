#!/usr/bin/python3


import os
import shutil
import time
import datetime
import json
from build_page import build_page
from config import py as cfg

# ripped from douglas/plugins/published_date.py
def parse_date(date_str):
    for fmt in ('%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M',
                '%Y-%m-%d'):
        try:
            return time.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError('time data {0} format is not recognized'.format(d))

def render_site():

    # naive file/folder creation here. Let's just 
    # assume everything works...

    # set up the output directory
    #os.mkdir(cfg['output_dir'])

    # copy over the static files and folders.
    # this is also where output_dir gets created! 
    shutil.copytree(cfg['static_dir'], cfg['output_dir'])

    # call build_page iteratively for each delve specified
    # in the config file. 
    for delve_id, delve in enumerate(cfg['delves']):
        print("Building data for delve %s" % delve['path_name'])

        # build a folder off root for the delve
        delve_dir = os.path.join(cfg['output_dir'], delve['path_name'])
        os.mkdir(delve_dir)
        # also build a folder for turns
        turn_dir = os.path.join(delve_dir, 'turn')
        os.mkdir(turn_dir)
        # ok, now crack open the index for the delve in focus
        index_loc = os.path.join(delve['dir_name'], 
                                       '%s.json' % delve['path_name'])
        with open(index_loc) as index_file:
            delve_index = json.load(index_file)
    
        # now clean up the index so that only published entries
        # are included. 
        cur_delve_index = []
        for turn in delve_index:
            if parse_date(turn['date']) < time.localtime():
                cur_delve_index.append(turn)
            else:
                print("Skipping turn %s, publish date is %s" %
                      (turn['turn'], turn['date']))

        # ** Warning. Keep clear the distinction between steps 
        # in the index of turns, and turn #. User-actionable turns 
        # in nethack do not always increment by 1!

        # collect required turn info from the set of valid turns
        
        # (this should probably *always* be 1)
        first = cur_delve_index[0]['turn']
        last = cur_delve_index[-1]['turn']
        
        # maybe this can be called with prev, cur, next syntax
        # to simplify? Not sure. 

        for turn_index, turn in enumerate(cur_delve_index):
            
            # go through the business of determining
            # previous and next turns. 
            # let's see if exceptions will handle this well
            if turn_index > 0:
                prv_move = cur_delve_index[turn_index-1]['turn']
            else:
                prv_move = 0

            try:
                nxt_move = cur_delve_index[turn_index+1]['turn']
            except:
                nxt_move = 0
                
            # now we have first nethack turn #, last nethack turn #, 
            # and previous and next turns for the current turn. 
            # time to generate the jinja template. 

            print("Publishing turn %s, publish date is %s" %
                  (turn['turn'], turn['date']))

            base_url = cfg['base_url'] + '/' + \
                       delve['path_name'] + '/' + \
                       'turn' 


            turn_html = build_page(delve_id=delve_id,
                                   turn=turn['turn'],
                                   first=first,
                                   prev=prv_move,
                                   next=nxt_move,
                                   last=last,
                                   date=turn['date'],
                                   delve_url=base_url)
                               
            turn_path = os.path.join(turn_dir,
                                     str(turn['turn']))
            os.mkdir(turn_path)

            turn_path = os.path.join(turn_path, 'index.html')

            with open(turn_path, mode='w', encoding='utf-8') as turn_file:
                turn_file.write(turn_html)
            
            # Fixme: This will need to be made more elegant. Brute-forcing
            # an index.html at site root temporarily.
            with open(os.path.join(cfg['output_dir'], 
                                   'index.html'),
                      mode='w',
                      encoding='utf-8') as turn_file:
                turn_file.write(turn_html)


if __name__ == '__main__':
    print("Generating static site for all delves")
    
    # bail if the static_render directory exists
    if os.path.exists(cfg['output_dir']):
        print("** Stopping. %s already exists **"% cfg['output_dir'])
    else:
        print("OK, let's do this.")
        render_site()
        
