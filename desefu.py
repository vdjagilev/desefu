#!/usr/bin/env python3

from colorama import init
from termcolor import colored

from kernel.config import Config
from kernel.kernel import Kernel
from kernel.output import Output, OutputResult
from kernel.result import Result

from time import strftime, localtime

_version = "0.2"
_choices = ['json', 'xml', 'csv', 'html']

# Initializing colorama
# Colors will be available in Windows CLI
init()

# Main method
if __name__ == '__main__':
    (options, args) = Kernel.start(_version, _choices)

    if options.module_info:
        Output.do("Getting information about module %s" % options.module_info)
        mod = Kernel.get_module('modules', options.module_info)
        yes_str = colored("Yes", "green")
        no_str = colored("No", "red")

        print(options.module_info)
        print("--------------------------------")
        print("")
        print(mod.description())
        print("")
        print("[%s]\tFile filtering" % (yes_str if mod.is_filter_files() else no_str))
        print("[%s]\tData collection" % (yes_str if mod.is_collect_data() else no_str))
        print("[%s]\tExtract data options" % (yes_str if mod.is_extract_data() else no_str))
        print("")
        Kernel.end()

    try:
        args[0]
        Output.do("Config file is: \"%s\"" % args[0])
    except IndexError:
        Output.fail("No config file specified. Exiting")
        Kernel.end()

    try:
        args[1]
        Output.do("Evidence root folder is: \"%s\"" % args[1])
    except IndexError:
        Output.fail("No evidence directory root folder specified. Exiting")
        Kernel.end()

    config = Config(args[0], args[1])
    module_chain_list = config.analyze()

    if len(module_chain_list) == 0:
        Output.fail("Module chain list is empty, there is no records in \"search\" field.")
        Kernel.end()

    # Executing search operation
    print(Output.do("Confirm if you want to start search (y/n): ", ret=True), end='')
    answer = input()

    result = Result(config)
    Kernel.result = result

    if answer.lower() == 'y':
        Output.ok("Search has been started")
        Kernel.exec_search(module_chain_list)
    else:
        Output.fail("Search has been cancelled")
        Kernel.end()

    result_filename = 'result_%s.json' % strftime('%d%m%Y_%H%M%S', localtime())
    result_file = open(result_filename, mode='w', encoding='utf-8')
    Output.do("Writing result data to %s" % result_filename)
    result_file.write(result.get_json())
    result_file.close()

    # Program END
    Kernel.end()
