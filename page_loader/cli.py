import argparse
import os


def parse():
    parser = argparse.ArgumentParser(
        description='Downloads website to a specified directory'
    )
    parser.add_argument('url')
    parser.add_argument('-o', '--output',
                        type=str, default=os.getcwd())
    args = parser.parse_args()
    return args
