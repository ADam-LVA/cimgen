import cimCodebaseGenerator
import os
import argparse
import importlib

parser = argparse.ArgumentParser(description='Generate some CIM classes.')
parser.add_argument('outdir', type=str, help='The output directory')
parser.add_argument('schemadir', type=str, help='The schema directory')
parser.add_argument('langdir', type=str, help='The langpack directory')
args = parser.parse_args()

print("build.py called with ", args)

langPack = importlib.import_module(args.langdir + ".langPack")

schema_path = os.path.join(os.getcwd(), args.schemadir)
cimCodebaseGenerator.cim_generate(schema_path, args.outdir, "cgmes_v2_4_15", langPack)

if args.langdir == "cpp":
    langPack.resolve_headers(args.outdir)
