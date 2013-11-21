#!/usr/bin/python

import sys


escape_chars = {
    "·": "&middot;",
    " ": "&nbsp;",
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

data = sys.stdin.readlines()

def escape(text):
    # ljust will make sure the string is 80 characters long
    clean_str = "".join(escape_chars.get(c,c) for c in text.ljust(80, " "))
    return clean_str

for line in data:
    print(escape(line)+"<br>")

