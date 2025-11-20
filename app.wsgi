import sys, os

## REDUNDANT #sys.path.insert(0, '/var/www/html/dash')

os.chdir('/var/www/html/dash')

print("wsgi: Current Working Directory:",os.getcwd())

from app import server as application

