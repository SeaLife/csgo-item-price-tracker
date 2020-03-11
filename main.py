import sys
import getopt
import logging

OPTIONS = {}
logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s')
LOG = logging.root
LOG.level = logging.INFO

opts, args = getopt.getopt(sys.argv[1:], "svpdlcr:", ['list', 'create', 'remove'])

for opt, arg in opts:
    if opt[:2] == '--':
        LOG.debug(f"OPTIONS['{opt[2:]}'] = {arg}")
        if arg == "":
            OPTIONS[opt[2:]] = True
        else:
            OPTIONS[opt[2:]] = arg
    else:
        LOG.debug(f"OPTIONS[{opt[1:]}] = {arg}")
        if opt[1:] == 'v':
            LOG.level -= 10
        if opt[1:] == 's':
            LOG.level += 10

        if arg == "":
            OPTIONS[opt[1:]] = True
        else:
            OPTIONS[opt[1:]] = arg

if 'p' in OPTIONS:
    import process

if 'd' in OPTIONS:
    import chart_generator

if 'c' in OPTIONS:
    import modify

    modify.create()

if 'l' in OPTIONS:
    import modify

    modify.list_items()

if 'r' in OPTIONS:
    import modify

    modify.remove_item(int(OPTIONS['r']))
