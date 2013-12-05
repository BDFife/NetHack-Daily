# #######################################################
# 
# This is the configuration file for the static site tools.
# You should review this file and fill in values when required. 
# The values will determine how the site is built. 
# 
# This file is python code and so must contain valid python
# syntax. 
#
# #######################################################


# Don't touch these next lines.
import os 
py = {}
SITEDIR ="/Users/Fife/Projects/NetHackaDay/"


# #################################
# Site configuration
#
# Below find parameters you may want to edit. 
#
# #################################

# Title of your site
py['site_title'] = "Nethack-a-Day"

# Short description of the site
py['site_description'] = "Nethack, one day at a time."

# Author(s) of the site
py['authors'] = "Brian Fife and Paul Nicklas"

# Email address where readers may contact the authors
py['site_email'] = "http://twitter.com/nethackaday"


# Copyright info for the site. This may be required to generate 
# a valid RSS feed. 
py['site_rights'] = "Some portions Copyright 2013 Brian Fife and Paul Nicklas"

# Primary language of the blog. This may be required to generate
# a valid RSS feed. 
py['site_language'] = "en"

# Encoding for the output. This defaults to utf-8.
py['site_encoding'] = "utf-8"

# Name, race, class and starting alignment of your character, as
# well as the folder name where related files are kept. 

# path_name is what the filesystem uses to ID the delve.
# only one delve should be featured. 
py['delves'] = [{ 'name':'Cody',
                  'race':'Human',
                  'class':'Tourist',
                  'alignment':'Neutral',
                  'path_name':'cody',
                  'dir_name':os.path.join(SITEDIR,'cody'),
                  'featured': True}]

# Location where the site's templates are kept. 
py['template_dir'] = os.path.join(SITEDIR, "templates")

# Base URL for the site. Useful if the site is not stored at the root
# of a domain. 
py['base_url'] = "http://nethackaday.com"

# Location where generated content should be stored. 
py['output_dir'] = os.path.join(SITEDIR, "compiled_site")

# Location where staging content should be stored.
py['staging_dir'] = os.path.join(SITEDIR, "staging")

# Base URL for staging directory
py['stage_url'] = "http://bluesock.org/~brian/nethack"

# Location of additional static files and folders that should be copied
# to the output_dir. 
py['static_dir'] = os.path.join(SITEDIR, "static_files")


