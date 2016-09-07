#!/usr/bin/env python3

from colorama import init

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
    analysis_result = config.analyze()

    if not analysis_result:
        Kernel.end()

    # Program END

    # Closing file
    if options.save_output and Output.file_resource:
        Output.log("Closing file with output")
        Output.file_resource.close()

    Kernel.end()
