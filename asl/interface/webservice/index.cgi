#!/usr/bin/python

# Append the right path to the PYTHONPATH for the CGI script to work.
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'));

from asl.interface import importer
importer.append_pythonpath()

# Now import the application and the remaining stuff.
from asl.application import service_application
from wsgiref.handlers import CGIHandler

from asl.interface.webservice import web_application_loader
web_application_loader.load()

# For WSGI.
application = service_application
service_application.initialize_dependencies()

# Run it!
if __name__ == "__main__":
    CGIHandler().run(service_application)