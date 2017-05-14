# Kernel module
# =============
import importlib
import sys, os
from optparse import OptionParser
from os.path import basename, join, splitext

from kernel.module_chain import ModuleChain
from kernel.output import Output, OutputResult
from modules import AbstractModule

from time import strftime, localtime


class Kernel:
    result = None
    options = None

    @staticmethod
    def start(_version):
        parser = OptionParser(usage="%prog [options] config_file directory_root", version="%prog " + _version)
        parser.add_option("-l", "--log", action="store_true", default=False,
                          help="Enable logging, which prints additional information the program is working right now")
        parser.add_option("-q", "--quiet", action="store_true", default=False,
                          help="Disable any output, except formatted one")
        parser.add_option("--save-output", action="store_true", default=False, help="Store output in a log file")
        parser.add_option("--module-info", default=None, help="Prints out module information")
        parser.add_option("--check", action="store_true", default=False, help="Check dependencies for modules")

        (options, args) = parser.parse_args()

        Output.logging = options.log
        Output.quiet = options.quiet

        if options.save_output:
            Output.log_file = 'result_%s.log' % strftime('%d%m%Y_%H%M%S', localtime())

        Output.do("Starting Desefu version %s" % _version, use_time=True)

        Kernel.options = options

        return options, args

    @staticmethod
    def check(check_path):
        Output.do("Perform general module check")

        for root, dirs, files in os.walk(check_path):
            path = root.split(os.sep)

            if '__pycache__' in path:
                continue

            for file in files:
                if file != '__init__.py':
                    module_name = splitext(basename(join(root, file)))[0]
                    full_name = join(os.sep.join(path[1:]), module_name).replace(os.sep, ".")

                    module = Kernel.get_module(check_path, full_name)
                    check_result = module.check()

                    if check_result:
                        Output.ok(full_name)
                    else:
                        Output.fail(full_name)

    @staticmethod
    def end():
        Output.do("Program end", use_time=True)
        try:
            if Kernel.options.save_output and Output.file_resource:
                Output.log("Closing file with output")
                Output.file_resource.close()
        except:
            pass
            
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
            module_data['title'] = mod.title

            if mod.extract_data:
                module_data['extract_data'] = mod.extract_data

            if mod.module_chain:
                module_data['module_chain'] = Kernel.collect_result(mod.module_chain)

            result['modules'].append(module_data)
            i += 1

        return result
