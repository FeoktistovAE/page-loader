import argparse
import os


def parse():
    parser = argparse.ArgumentParser(
        description='Downloads web page to a specified directory'
    )
    parser.add_argument('url')
    parser.add_argument(
        '-o', '--output', type=str, default=os.getcwd()
    )
    return parser.parse_args()
