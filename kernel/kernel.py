# Kernel module
# =============
import importlib
import sys
from optparse import OptionParser

from kernel.module_chain import ModuleChain
from kernel.output import Output, OutputResult
from modules import AbstractModule


class Kernel:
    result = None

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
        parser.add_option("--module-info", default=None, help="Prints out module information")

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

        Output.do("Starting Desefu version %s" % _version)

        return options, args

    @staticmethod
    def end():
        Output.do("Program end", result=OutputResult.Info)
        sys.exit()

    @staticmethod
    def get_module(module_type: str, name: str) -> AbstractModule:
        mod = None

        # Module import & Initialization
        try:
            mod_import = importlib.import_module(module_type + '.' + name)
            mod_class = getattr(mod_import, name.split('.').pop())

            mod = mod_class()
        except ImportError as e:
            Output.err("Could not import module \"%s\"" % name)
            Output.log(e)
            Kernel.end()
        except TypeError as e:
            Output.err("Could not initialize module. Important functions are missing in module")
            Output.log(e)
            Kernel.end()

        return mod

    @staticmethod
    def exec_search(module_chain: list, sub: bool = False, parent_chain: ModuleChain = None) -> list:
        for mc in module_chain:
            Output.do("Running module chain: \"%s\"" % mc.id)
            Output.do("Amount of files: %d" % len(mc.files))

            for mod in mc.modules:
                mod.files = mc.files

                if sub:
                    mod.parent_module_chain = parent_chain

                mod.execute()

                mc.files = mod.files

                if mod.module_chain:
                    Output.log("Running submodules of %s" % mod.__class__.__module__.replace("modules.", "", 1))
                    # Setting parent module chain
                    mod.module_chain.files = mod.files
                    Kernel.exec_search([mod.module_chain], True, mc)

            if not sub:
                module_chain_result = Kernel.collect_result(mc)
                Kernel.result.result.append(module_chain_result)

    @staticmethod
    def collect_result(module_chain: ModuleChain) -> object:
        result = {
            "module_chain_id": module_chain.id,
            "modules": []
        }

        i = 0
        m = len(module_chain.modules)
        for mod in module_chain.modules:
            module_data = {
                'mod': mod.__class__.__module__.replace("modules.", "", 1)
            }

            # It makes sense to include files only for the last module
            # when all of them were filtered in certain Module Chain
            if i == (m - 1):
                module_data['files'] = mod.files

            module_data['files_count'] = len(mod.files)
            module_data['data'] = mod.data

            if mod.extract_data:
                module_data['extract_data'] = mod.extract_data

            if mod.module_chain:
                module_data['module_chain'] = Kernel.collect_result(mod.module_chain)

            result['modules'].append(module_data)
            i += 1

        return result
