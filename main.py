import sys
import getopt

from lib.dto import Context

ctx = Context()

print(sys.argv)

opts, args = getopt.getopt(sys.argv[1:], "lcr:", ['list', 'create', 'remove'])

print(opts)

for opt, arg in opts:
    if opt[:2] == '--':
        ctx.set_attribute(opt[2:], arg)
    else:
        ctx.set_attribute(opt[1:], arg)
