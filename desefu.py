#!/usr/bin/env python3

from colorama import init
from termcolor import colored

from kernel.config import Config
from kernel.kernel import Kernel
from kernel.output import Output, OutputResult

_version = "0.1a"
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

        print(mod.description())
        print("[%s]\tFile filtering" % (yes_str if mod.is_filter_files() else no_str))
        print("[%s]\tData collection" % (yes_str if mod.is_collect_data() else no_str))
        print("[%s]\tExtract data options" % (yes_str if mod.is_extract_data() else no_str))
        Kernel.end()

    try:
        args[0]
        Output.do("Config file is: \"%s\"" % args[0])
    except IndexError:
        Output.do("No config file specified. Exiting", result=OutputResult.Fail)
        Kernel.end()
    
    try:
        args[1]
        Output.do("Evidence root folder is: \"%s\"" % args[1])
    except IndexError:
        Output.do("No evidence directory root folder specified. Exiting", result=OutputResult.Fail)
        Kernel.end()

    config = Config(args[0], args[1])
    module_chain_list = config.analyze()

    # After all analysis is done and config file has been parsed
    # Run needed
    config.close()

    if len(module_chain_list) == 0:
        Output.do("Module chain list is empty, there is no records in \"search\" field.", OutputResult.Fail)
        Kernel.end()

    for mc in module_chain_list:
        Output.log("Running module chain (ID: %s)" % mc.id)

    # Program END

    # Closing file
    if options.save_output and Output.file_resource:
        Output.log("Closing file with output")
        Output.file_resource.close()

    Kernel.end()
