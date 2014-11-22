#!/usr/bin/env python

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'));

from asl.interface.importer import append_pythonpath
append_pythonpath()
from asl.interface.webservice import web_application_loader
web_application_loader.load()

# Now import the application and the remaining stuff.
from asl.application import service_application
service_application.initialize_dependencies()

from asl.utils.deploy.js_model_generator import ModelGenerator
from asl.utils.deploy.integrator import integrate_to_file

import argparse
import hashlib

parser = argparse.ArgumentParser(description="Export python models to Backbone.js")
parser.add_argument("module", help="module from which models are imported")
parser.add_argument("models", metavar="model", help="model name, can be a tuple WineCountry/WineCountries as singular/plural", nargs="+")
parser.add_argument("-mp", "--model-prefix", help="namespace prefix for models (Feminity.models.)")
parser.add_argument("-cp", "--collection-prefix", help="namespace prefix for collection (Feminity.collections.)")
parser.add_argument("-m", "--model-fn", help="name of model constructor (Atteq.bb.Model)")
parser.add_argument("-c", "--collection-fn", help="name of collection constructor (Atteq.bb.Collection)")
parser.add_argument("--marker", help="marker to indicate the autogenerated code")
parser.add_argument("-i", "--integrate", help="integrate to file") # inegruj ked optional

def parse_model_arg(models):
    return [tuple(m.split('/')) if '/' in m else m for m in models]


# Run it!
if __name__ == "__main__":
    args = parser.parse_args()

    kwargs = vars(args).copy()

    del kwargs['models']
    del kwargs['marker']

    generator = ModelGenerator(**{ k: kwargs[k] for k in kwargs if kwargs[k]}) # odstranime None value

    models = generator.generate_models(parse_model_arg(args.models))

    if args.integrate:
        sys.stderr.write("Integrate is really experimental")
        sys.exit(1)
        
        if args.marker:
            marker = args.marker
        else:
            marker = hashlib.md5("{0}{1}".format(args.module, args.models)).hexdigest()
    
        start = "// * -- START AUTOGENERATED %s -- * //\n" % marker
        end = "// * -- END AUTOGENERATED %s -- * //\n" % marker
        integrate_to_file("\n".join(models), args.file, start, end)
         
    else: 
        print "\n".join(models)