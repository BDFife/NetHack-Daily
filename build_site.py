#!/usr/bin/python
# _*_ coding: utf-8 _*_

import sys
import os
import codecs
import shutil
import time
import datetime
import json
from build_page import build_page
from config import py as cfg
from jinja2 import Environment, FileSystemLoader
from email.Utils import formatdate

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

def render_site(output_dir, staging=False, prod=False):

    # naive file/folder creation here. Let's just 
    # assume everything works...

    # set up the output directory
    #os.mkdir(cfg['output_dir'])

    # copy over the static files and folders.
    # this is also where output_dir gets created! 
    shutil.copytree(cfg['static_dir'], output_dir)

    # call build_page iteratively for each delve specified
    # in the config file. 
    for delve_id, delve in enumerate(cfg['delves']):
        print("Building data for delve %s" % delve['path_name'])

        # build a folder off root for the delve
        delve_dir = os.path.join(output_dir, delve['path_name'])
        os.mkdir(delve_dir)
        # also build a folder for turns
        turn_dir = os.path.join(delve_dir, 'turn')
        os.mkdir(turn_dir)
        # build a folder for story and tip files
        story_dir = os.path.join(delve_dir, 'stories')
        os.mkdir(story_dir)
        tip_dir = os.path.join(delve_dir, 'tips')
        os.mkdir(tip_dir)

        # ok, now crack open the index for the delve in focus
        index_loc = os.path.join(delve['dir_name'], 
                                       '%s.json' % delve['path_name'])
        with codecs.open(index_loc) as index_file:
            delve_index = json.load(index_file)

        if not staging: 
            # now clean up the index so that only published entries
            # are included. 
            cur_delve_index = []
            for turn in delve_index:
                if parse_date(turn['date']) < time.localtime():
                    cur_delve_index.append(turn)
                else:
                    print("Skipping turn %s, publish date is %s" %
                          (turn['turn'], turn['date']))
        
        else:
            cur_delve_index = delve_index

        # These are for the rss feed:
        rss_list = []

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
                
            multi = cur_delve_index[turn_index]['multi']
                
            # now we have first nethack turn #, last nethack turn #, 
            # and previous and next turns for the current turn
            # as well as whether there are multiple actions in turn. 
            # time to generate the jinja template. 

            print("Publishing turn %s, publish date is %s" %
                  (turn['turn'], turn['date']))

            base_url = cfg['base_url'] + '/' + \
                       delve['path_name'] + '/' + \
                       'turn' 

            time_str = time.strftime("%B %d, %Y", parse_date(turn['date']))
            
            turn_html, turn_story, turn_tip  = build_page(delve_id=delve_id,
                                                          turn=turn['turn'],
                                                          first=first,
                                                          prev=prv_move,
                                                          next=nxt_move,
                                                          last=last,
                                                          date=time_str,
                                                          delve_url=base_url,
                                                          multi=multi,
                                                          prod=prod)
                               
            turn_path = os.path.join(turn_dir,
                                     str(turn['turn']))
            os.mkdir(turn_path)

            turn_path = os.path.join(turn_path, 'index.html')

            with codecs.open(turn_path, mode='w', 
                             encoding='utf-8') as turn_file:
                turn_file.write(turn_html)
            
            # Fixme: This will need to be made more elegant. Brute-forcing
            # an index.html at site root temporarily.
            with codecs.open(os.path.join(output_dir, 'index.html'),
                             mode='w',
                             encoding='utf-8') as turn_file:
                turn_file.write(turn_html)


            # Fixme: This shouldn't work, I think after multiple 
            # delves are included. 
            # Now take care of the RSS feed. Inefficient!
            rss_list.append({'turn':turn['turn'],
                             'date':time_str,
                             'rfc822date':formatdate(time.mktime(parse_date(turn['date']))),
                             'path':base_url + '/' + str(turn['turn']),
                             'tip':turn_tip,
                             'story':turn_story,})

            # Do the Jinja2 stuff for the RSS generation:
            env = Environment(loader=FileSystemLoader(cfg['template_dir']))
            template = env.get_template('default.rss', globals=cfg)
            
            rss_feed = template.render(content = rss_list[-20:],
                                       latest_rfc822date = formatdate())
            
            with codecs.open(os.path.join(output_dir, 'default.rss'),
                             mode='w',
                             encoding='utf-8') as rss_file:
                rss_file.write(rss_feed)

            # Use the RSS feed construct to build the tip and story feeds as well.
            tips = []
            stories  = []
            for turn in rss_list:
                tips.append([base_url + '/' + str(turn['turn']), 
                             turn['turn'],
                             turn['tip']])
                stories.append([base_url + '/' + str(turn['turn']), 
                                turn['turn'],
                                turn['story']])
            
            template = env.get_template('delve_list.html', globals=cfg)
            
            story_list = template.render(list_type="Stories", 
                                         list_items=stories)
            
            with codecs.open(os.path.join(story_dir, 'index.html'),
                             mode='w',
                             encoding='utf-8') as story_file:
                story_file.write(story_list)

            tip_list = template.render(list_type="Tips",
                                       list_items=tips)
            
            with codecs.open(os.path.join(tip_dir, 'index.html'),
                             mode='w',
                             encoding='utf-8') as tip_file:
                tip_file.write(tip_list)
            
            
if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == "stage":
        print("Generating staging site for all delves")
        cfg['base_url'] = cfg['stage_url']
        # bail if the static_render directory exists
        if os.path.exists(cfg['staging_dir']):
            print("** Stopping. %s already exists **"% cfg['staging_dir'])
        else:
            print("OK, let's do this.")
            render_site(cfg['staging_dir'], staging=True)
            
    # This is specifically to include tracking/analytics
    elif len(sys.argv) > 1 and sys.argv[1] == "prod":
        print("Generating production site for all delves")

        # bail if the static_render directory exists
        if os.path.exists(cfg['output_dir']):
            print("** Stopping. %s already exists **"% cfg['output_dir'])
        else:
            print("OK, let's do this.")
            render_site(cfg['output_dir'], staging=False, prod=True)
        
    else:    
        print("Generating static site for all delves")
    
        # bail if the static_render directory exists
        if os.path.exists(cfg['output_dir']):
            print("** Stopping. %s already exists **"% cfg['output_dir'])
        else:
            print("OK, let's do this.")
            render_site(cfg['output_dir'], staging=False, prod=False)
        
