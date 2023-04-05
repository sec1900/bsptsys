"""
@description:
@author:baola
@time:2022/4/12 19:54
@Python_version: 3.8.5
"""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', help="increase output verbosity", action='store_true')
args = parser.parse_args()
if args.verbose:
    print('yes')