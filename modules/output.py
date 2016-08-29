from termcolor import colored
from time import strftime, localtime

class OutputResult:
    OK = ('+', 'green', ['bold'])
    Fail = ('-', 'red', ['bold'])
    Info = ('i', 'blue', ['bold'])

    Warn = ('WRN', 'yellow', ['bold'])
    Error = ('ERR', 'red', ['bold'])
    Log = ('LOG', None, ['bold'])

class Output:
    logging = False
    quiet = False
    current_format = None
    date_format = "%x %X %z"
    log_file = None
    file_resource = None

    def do(message, result=OutputResult.Info, use_time=True):
        if Output.log_file and Output.file_resource is None:
            Output.file_resource = open(Output.log_file, 'w+')

        if Output.quiet:
            return

        print('[', end='')
        print(colored(result[0], result[1], attrs=result[2]), end='')
        print('] ', end='')

        if Output.log_file:
            Output.file_resource.write('[%s] ' % result[0])

        if use_time:
            print('[%s] ' % strftime(Output.date_format, localtime()), end='')

            if Output.log_file:
                Output.file_resource.write('[%s] ' % strftime(Output.date_format, localtime()))

        print(message)
        
        if Output.log_file:
            Output.file_resource.write(message + '\n')

    def log(message):
        if Output.quiet:
            return

        if Output.logging == True:
            Output.do(message, result=OutputResult.Log)
