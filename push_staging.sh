git pull
rm -rf ./staging
/home/brian/.virtualenvs/netHackaDay/bin/python ./build_site.py stage
rm -rf ~/public_html/nethack/*
cp -r ./staging/* ~/public_html/nethack
