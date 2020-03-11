import sys
import getopt
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s')
LOG = logging.root
LOG.level = logging.INFO


def process_arg(option, argument):
    if option == 'p' or option == 'process':
        import process

    if option == 'd' or option == 'generate-charts':
        import chart_generator

    if option == 'c' or option == 'create':
        import modify

        modify.create()

    if option == 'l' or option == 'list':
        import modify

        modify.list_items()

    if option == 'r' or option == 'remove':
        import modify

        modify.remove_item(int(argument))

    if option == 'v':
        LOG.level -= 10

    if option == 's':
        LOG.level += 10

    if option == 'h' or option == 'help':
        print(f"Usage {sys.argv[0]} -svpdlchr")
        print(" options:")
        print("  -h, --help             displays this help information")
        print("  -v                     increases the log level by 10")
        print("  -s                     decreases the log level by 10")
        print("  -p, --process          runs the processor to fetch prices from Steam and SkinBaron")
        print("  -c, --create           interactive creation of a weapon")
        print("  -l, --list             lists all items")
        print("  -r, --remove [id]      removes the weapon by id")
        print("  -d, --generate-charts  generates the charts and sends them per mail")
        print(" ")
        exit(0)


try:
    opts, args = getopt.getopt(sys.argv[1:], "svpdlchr:",
                               ['help', 'process', 'generate-charts', 'list', 'create', 'remove='])
except getopt.GetoptError:
    process_arg('h', True)
    exit(0)

for opt, arg in opts:
    if opt[:2] == '--':
        LOG.debug(f"OPTIONS['{opt[2:]}'] = {arg}")
        process_arg(opt[2:], arg or True)
    else:
        LOG.debug(f"OPTIONS[{opt[1:]}] = {arg}")
        process_arg(opt[1:], arg or True)

if len(sys.argv) == 1:
    process_arg('h', True)
