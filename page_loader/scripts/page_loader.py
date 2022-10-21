#!/usr/bin/env python


from page_loader import download
from page_loader.cli import parse


def main():
    args = parse()
    print(download(args.url, path=args.output))


if __name__ == '__main__':
    main()
