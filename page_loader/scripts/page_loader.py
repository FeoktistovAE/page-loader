#!/usr/bin/env python


from page_loader import download
from page_loader.cli import parse
import logging


logging.basicConfig()
logger = logging.getLogger()


def main():
    args = parse()
    print(download(args.url, path=args.output))


if __name__ == '__main__':
    main()
