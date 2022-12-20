#!/usr/bin/env python


from page_loader import download
from page_loader.cli import parse
import logging
import sys
import requests


logging.basicConfig()
logger = logging.getLogger()


def main():
    try:
        args = parse()
        print(download(args.url, path=args.output))
        sys.exit(0)
    except requests.exceptions.InvalidURL as e:
        logger.debug(e)
    except requests.exceptions.ConnectionError as e:
        logger.debug(e)
        logging.error('Не удалось загрузить страницу')
    except requests.exceptions.MissingSchema as e:
        logging.debug(e)
        logging.error(f'Отсутсвует схема в набранном URL, возможно вы имели в виду http://{args.url}?')
    except OSError as e:
        logging.debug(e)
        logging.error(f'Директории "{args.output}" не существует, либо к ней ограничен доступ')
    sys.exit(1)


if __name__ == '__main__':
    main()
