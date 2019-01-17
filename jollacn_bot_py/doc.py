"""
Usage:
    python_bot_py [options] twitter_fetcher

Options:
    -c, --config=<file>     config file path. [default: config.json]
"""


import docpie


def parse():
    return docpie.docpie(__doc__)


if __name__ == '__main__':
    print(parse())
