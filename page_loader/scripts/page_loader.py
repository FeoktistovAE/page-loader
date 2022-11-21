#!/usr/bin/env python


from page_loader import download
from page_loader.cli import parse
from page_loader.downloader import KnownError
import logging
import sys


logging.basicConfig()
logger = logging.getLogger()


def main():
    try:
        args = parse()
        print(download(args.url, path=args.output))
        sys.exit(0)
    except KnownError:
        sys.exit(1)


if __name__ == '__main__':
    main()
