import sys

if sys.version_info[0] < 3:
    from codecs import open
else:
    open = open  # for import


del sys
