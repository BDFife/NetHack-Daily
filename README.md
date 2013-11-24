# NetHackaDay

## Overview

The intent of this project is:
    1) Collect tools required for the nethack-a-day site
    2) Back up game states and interim files as they are created

## Goal of the Site

Capture a NetHack game turn-by-turn. Easy, right? 

I am developing tools that will take a copied 'screen shot' from a
NetHack terminal session and turn it into valid HTML. I am also
developing structure and styling that simplifies rendering a NetHack
game page. 

I don't have a good automated way (at this time) to capture inventory
or the long-form descriptions automatically. At the moment, I'm
copying them over by hand. 

I would also like to include two other elements from each page - a
color commentary narrative written by a guest author, and 'spoiler'
player commentary that plays a tip-of-the-day role. 

## Things to do

Switch to the \<pre\> tag instead of \<code\>
Consider dropping the HTML space characters
Update the CSS in the repository to match what is live on site
Make the hover blocks less translucent
Change the hover for inventory to float 'up' rather than down.
Determine why firefox browser behaves strangely when using hover (due
to interaction with the web host CSS and my local CSS)

## Things to remember

Save files are stored at /usr/games/lib/nethackdir/ on my computer. 

## HTML Snippets:

\<a href=# class="inv"\>[I]\<span\>INV\</span\>

\<a href=# class="det"\>@\<span\>DESC\</span\>

## Friends who have helped us: 

Will Kahn-Greene
