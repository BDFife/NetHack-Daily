#!/usr/bin/python

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

"""
Walks through the nethack 'screen shot' and replaces problematic
symbols with HTML-safe versions, and pads the lines out to 80 chars

Uses escape_chars as a reference table.
"""
def escape(text):
    # ljust will make sure the string is 80 characters long
    # make sure to trim out the trailing newline.
    full_text = text[:-1].ljust(80, " ")
    clean_str = "".join(escape_chars.get(c,c) for c in full_text)
    return clean_str

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: handle_url.py [turn number]")
    else:
        turn = sys.argv[1]
        print("Processing data for turn %s" % turn)
        
        # import the screenshot data
        with open('%s.nss' % turn) as scr_file:
            scr_data = scr_file.readlines()
            # hack in my 'inventory' tag to the last line.
            scr_data[-1] = scr_data[-1][:-1] + " [I]\n"
        # opening tags
        htm_data = [
            '<div class="netHackScr">',
            '<hr>',
            '<pre>',
        ]

        # process the screenshot data
        for line in scr_data:
            htm_data.append(escape(line))

        # make sure the pre close tag is appended to the last line
        # then add the other closing tags
        htm_data[-1] = htm_data[-1] + '</pre>'    
        htm_data.append('<hr>')
        htm_data.append('</div> <!-- netHackScr -->')

        # convert the list to a string in sections:
        # header, body, footer
        htm_header = "\n".join(htm_data[0:3])
        htm_body = "\n".join(htm_data[4:-2])
        htm_footer = "\n".join(htm_data[-2:])
   
        # add in the inventory and object descriptions
        with open('%s.inv' % turn) as inv_file:
            inv_data = inv_file.readlines()
        
        with open('%s.inv' % turn) as obj_file: 
            obj_data = obj_file.readlines()

        full_htm_data = ""
        
        # naturally, this will have to be filled out soon!
        obj_list = "@(+d"
        obj_counter = 0
        
        # replace an 'object of interest' with the marked up 
        # description text
        for char in htm_body:
            if char in obj_list:
                print(char)
                href_str = '''<a href=# class="det">%s<div>%s</div></a>''' % (char, obj_data[obj_counter])
                obj_counter += 1
                full_htm_data += href_str
            else:
                full_htm_data += char

        # export the file
        print(htm_data)

