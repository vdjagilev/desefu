# Kernel module
# =============
from optparse import OptionParser

from kernel.output import Output, OutputResult


class Kernel:
    @staticmethod
    def start(_version, _choices):
        parser = OptionParser(usage="%prog [options] config_file directory_root", version="%prog " + _version)
        parser.add_option("-l", "--log", action="store_true", default=False,
                          help="Enable logging, which prints additional information the program is working right now")
        parser.add_option("-q", "--quiet", action="store_true", default=False,
                          help="Disable any output, except formatted one")
        parser.add_option("--format", default=None, choices=_choices,
                          help="Result is being shown in specific format %s" % _choices)
        parser.add_option("--date-format", default=None,
                          help="Date format which is used for all output which is made to console, all required symbols can be found at https://docs.python.org/3.5/library/time.html#time.strftime. \nBy default locale appropriate time representation is done.")
        parser.add_option("--save-output", default=None, help="Store output in a log file")

        (options, args) = parser.parse_args()

        Output.logging = options.log
        Output.quiet = options.quiet
        Output.current_format = options.format

        if options.save_output is not None:
            Output.log_file = options.save_output

        if Output.current_format is not None:
            Output.quiet = True

        if options.date_format is not None:
            Output.date_format = options.date_format

        Output.log("Start program")
        Output.do("Starting Desefu version %s" % _version)

        return options, args

    @staticmethod
    def end():
        Output.do("Program end", result=OutputResult.Info)
        exit()
