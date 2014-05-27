git pull
rm -rf ./compiled_site
/home/brian/.virtualenvs/netHackaDay/bin/python ./build_site.py prod
rm -rf ~/sites/netHackaDay/*
cp -r ./compiled_site/* ~/sites/netHackaDay
