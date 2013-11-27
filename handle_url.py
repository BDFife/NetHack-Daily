#!/usr/bin/python3

import sys

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

def build_header(turn=1, date="January 1, 2014"):
    
    html_header = [
        '<html>',
        '\t<head>', 
        '\t\t<link rel="stylesheet" href="netHackDaily.css" type="text/css" />',
        '\t\t<title>Nethack-a-Day</title>',
        '\t</head>',
        '\t<body>',
        '\t\t<div class="wrap">',
        '\t\t\t<h1>Hethack-@-Day</h1>',
        '\t\t\t<h2>Nethack, one day at a time.</h2>',
        '\t\t\t<div class="turn_title"> Turn %s </div>'% turn,
        '\t\t\t<div class="date">%s</div>'% date,
        '\t\t\t<div class="netHackScr">',
        '<!-- The following section must not be indented or it will mess up the ' +
        '<pre> rendering -->',
        ]

    return html_header

def build_footer(prev_turn=1, next_turn=2, 
                 story="story goes here", tip="tip goes here"):

    html_footer = [
        '\t\t\t</div> <!-- netHackScr -->',
        '\t\t\t<div class="comments">',
        '\t\t\t\t<div class="story">',
        '\t\t\t\t\t<p>%s</p>'% story,
        '\t\t\t\t</div> <!-- story -->',
        '\t\t\t\t<div class="tip">',
        '\t\t\t\t\t<p>%s</p>'% tip,
        '\t\t\t\t</div> <!-- tip -->',
        '\t\t\t</div> <!-- comments -->',
        '\t\t\t<div class="footer">',
        '\t\t\t\t<ul class="nav">',
        '\t\t\t\t\t<li>First</li>',
        '\t\t\t\t\t<li>Previous</li>',
        '\t\t\t\t\t<li>Next</li>',
        '\t\t\t\t\t<li>Current</li>',
        '\t\t\t\t</ul> <!-- nav -->',
        '\t\t\t</div> <!-- footer -->',
        '\t\t</div> <!-- wrap -->', 
        '\t</body>',
        '</html>',
        ]
    
    return html_footer

def build_page(turn=1, prev=1, next=2, date="January 1, 2013"):

    # import the screenshot data
    with open('%s.nss' % turn) as scr_file:
        scr_data = scr_file.readlines()
        # hack in my 'inventory' tag to the last line.
        scr_data[-1] = scr_data[-1].rstrip('\n') + " [I]\n"

    # Now build the netHack 'screenshot' as a <pre> section
    # utf-8 shapes must be escaped and all lines must be padded to 80 chars
    # we are also drawing a box around the 'screenshot'
    #
    # The order of operations is going to look a little dysfunctional.
    # the NetHack screen can be divided into three sections:
    #
    # The header section includes some text/status messages, and the 
    # border. Except for the border, it will not contain characters that must
    # be HTML-escaped.
    # 
    # The body section is where the 'map' and any items/monsters are drawn.
    # this section may contain HTML-unsafe characters like <, > *and* includes
    # objects and monsters that require a description.
    # 
    # The footer section includes the two attribute bars. We have also added a 
    # special character, [I], that is used to show the player's inventory. 
    # Finally, the bottom border is also drawn. Except for the border, it will
    # not contain characters that must be HTML-escaped. 
    
    # generate the 'fixed' entry HTML header code. 
    # the only dynamic elements are turn # and date.
    htm_data = build_header(turn=turn, date=date)
    
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
    htm_header = "\n".join(htm_data[0:15])
    htm_body = "\n".join(htm_data[15:-3])
    htm_footer = "\n".join(htm_data[-3:])

    # add in the inventory and object descriptions
    with open('%s.inv' % turn) as inv_file:
        inv_data = inv_file.readlines()
    
    with open('%s.obj' % turn) as obj_file: 
        obj_data = obj_file.readlines()

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

    # here's a sneaky trick. Make the alignment identifier a tag without a label to 
    # 'clear' hover text on touch devices.
    # there *must* be a more elegant way to do this in python.
    htm_footer = htm_footer.replace('Lawful', '<a href=# class="det">Lawful</a>')
    htm_footer = htm_footer.replace('Neutral', '<a href=# class="det">Neutral</a>')
    htm_footer = htm_footer.replace('Chaotic', '<a href=# class="det">Chaotic</a>')

    full_htm_data += "\n" + htm_footer
    
    with open('%s.str' % turn) as str_file:
        str_data = str_file.read()
    
    with open('%s.tip' % turn) as tip_file:
        tip_data = tip_file.read()
    
    html_footer = build_footer(prev_turn=prev, next_turn=next,
                               story=str_data, tip=tip_data)
                               
    full_htm_data += "\n".join(html_footer)

    return full_htm_data

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: handle_url.py [turn number]")
    else:
        turn = sys.argv[1]
        #print("Processing data for turn %s" % turn)
        
        print(build_page(turn=turn))