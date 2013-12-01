#!/usr/bin/python3

import sys
import os
from config import py as cfg
from jinja2 import Environment, FileSystemLoader

# These are the nethack characters that must be html-escaped
escape_chars = {
    "·": "&middot;",
    " ": " ", # not using &nbsp anymore
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    "┌": "&#9484;",
    "─": "&#9472;",
    "┐": "&#9488;",
    "│": "&#9474;",
    "└": "&#9492;",
    "┘": "&#9496;",
    }

def build_nethack_section(nss, obj, inv):
    # Takes in the data from [turn].nss.readlines()

    # Builds the netHack 'screenshot' as a <pre> section
    # utf-8 shapes must be escaped and all lines must be padded to 80 chars
    # we are also drawing a box around the 'screenshot'
    #
    # The order of operations is going to look a little dysfunctional.
    # the NetHack screen can be divided into three sections:
    #
    # The header section includes some text/status messages, and the 
    # border. Except for the border, the header will not contain characters 
    # that must be HTML-escaped.
    # 
    # The body section is where the 'map' and any items/monsters are drawn.
    # this section may contain HTML-unsafe characters like <, > *and* includes
    # objects and monsters that require a description.
    # 
    # The footer section includes the two attribute bars. We have also added a 
    # special character, [I], that is used to show the player's inventory. 
    # Finally, the bottom border is also drawn. Except for the border, the 
    # footer will not contain characters that must be HTML-escaped. 

    scr_data = nss

    ###
    # Draw the nethack screen.
    ###

    # hack in my 'inventory' tag to the last line.
    scr_data[-1] = scr_data[-1].rstrip('\n') + " [I]\n"

    htm_data = []

    # begin the <pre> section and draw the top frame. 
    top_str = '<pre>' + '&#9484;' + ('&#9472;' * 80 ) + '&#9488;'
    htm_data.append(top_str)
  
    # take the special-case status line
    status_str = scr_data[0].rstrip('\n')
    status_str = status_str.ljust(80, " ")
    htm_data.append('&#9474;' + status_str + '&#9474;')

    # now run through the actual screenshot data
    for line in scr_data[1:-2]:
        tmp_line = line.rstrip('\n')
        tmp_line = tmp_line.ljust(80, " ")
        htm_data.append("│" + tmp_line + "│")

    for line in scr_data[-2:]:
        tmp_line = line.rstrip('\n')
        tmp_line = tmp_line.ljust(80, " ")
        htm_data.append('&#9474;' + tmp_line + '&#9474;')

    # add the bottom frame line and close the <pre> section
    bot_str = '&#9492;' + ('&#9472;' * 80) + '&#9496;' + '</pre>'
    htm_data.append(bot_str)
    
    # convert the list of strings to a single string.
    # keep header, body, footer separate. 
    htm_header = "\n".join(htm_data[0:2])
    htm_body = "\n".join(htm_data[2:-3])
    htm_footer = "\n".join(htm_data[-3:])

    ###
    # Convert all characters to html-safe, and add object descriptions.
    ###

    inv_data = inv
    obj_data = obj

    full_htm_data = ""
    full_htm_data += htm_header + '\n'

    # naturally, this will have to be filled out fully soon!
    obj_list = "<@)+d"
    obj_counter = 0

    # replace an 'object of interest' with the marked up 
    # description text
    for char in htm_body:
        if char in obj_list:
            if char in escape_chars:
                char = escape_chars[char]
            # don't forget to snip the newline from obj_counter.
            href_str = '''<a href=# class="det">%s<div>%s</div></a>''' \
                          % (char, obj_data[obj_counter].rstrip('\n'))
            obj_counter += 1
            full_htm_data += href_str
        else:
            if char in escape_chars:
                char = escape_chars[char]
            full_htm_data += char

    # fix out the [I] tag.
    inv_block = "".join(inv_data)        
    htm_footer = htm_footer.replace('[I]',"""<a href=# class="inv">[I]<div>%s</div></a>""" % inv_block)

    # here's a sneaky trick. Make the alignment identifier a tag
    # without a label to 'clear' hover text on touch devices.
    # there *must* be a more elegant way to do this in python.

    htm_footer = htm_footer.replace('Lawful', 
                                    '<a href=# class="det">Lawful</a>')
    htm_footer = htm_footer.replace('Neutral', 
                                    '<a href=# class="det">Neutral</a>')
    htm_footer = htm_footer.replace('Chaotic',
                                    '<a href=# class="det">Chaotic</a>')

    full_htm_data += "\n" + htm_footer
    return full_htm_data

def build_page(delve_id=0, 
               turn=1, 
               first=1,
               prev=0, 
               next=2, 
               last=2,
               date="January 1, 2013",
               delve_url="/"):

    delve_dir = cfg['delves'][0]['dir_name']

    # import the screenshot data
    with open(os.path.join(delve_dir, '%s.nss' % turn)) as scr_file:
        scr_data = scr_file.readlines()

    # add in the inventory and object descriptions
    with open(os.path.join(delve_dir, '%s.inv' % turn)) as inv_file:
        inv_data = inv_file.readlines()
    
    with open(os.path.join(delve_dir, '%s.obj' % turn)) as obj_file: 
        obj_data = obj_file.readlines()

    body = build_nethack_section(scr_data, obj_data, inv_data)
    
    with open(os.path.join(delve_dir,'%s.str' % turn)) as str_file:
        str_data = str_file.read()
    
    story = str_data
    
    with open(os.path.join(delve_dir,'%s.tip' % turn)) as tip_file:
        tip_data = tip_file.read()
    
    tip = tip_data
    
    env = Environment(loader=FileSystemLoader(cfg['template_dir']))
    template = env.get_template('game_state.html', globals=cfg)
    
    nav ='<ul class="nav"><li>First Turn</li><li>Previous Turn</li><li>Next Turn</li><li>Current Turn</li></ul>'
    
    return(template.render(date=date,
                           turn=turn,
                           entry=body,
                           story=story,
                           tip=tip,
                           first=first,
                           prev=prev,
                           next=next,
                           last=last,
                           delve_url=delve_url)) 

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: handle_url.py [delve number] [turn number]")
    else:
        delve = sys.argv[1]
        turn = sys.argv[2]
        print(build_page(delve_id=delve, turn=turn))
