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
    date_format = "%X"
    log_file = None
    file_resource = None

    @staticmethod
    def ok(message: str, use_time: bool = True):
        Output.do(message, OutputResult.OK, use_time)

    @staticmethod
    def fail(message: str, use_time: bool = True):
        Output.do(message, OutputResult.Fail, use_time)

    @staticmethod
    def warn(message: str, use_time: bool = True):
        Output.do(message, OutputResult.Warn, use_time)

    @staticmethod
    def err(message: str, use_time: bool = True):
        Output.do(message, OutputResult.Error, use_time)

    @staticmethod
    def do(message: str, result: tuple = OutputResult.Info, use_time: bool = True, ret: bool = False):
        if Output.log_file and Output.file_resource is None:
            Output.file_resource = open(Output.log_file, 'w+')

        if Output.quiet:
            return

        date_time = ""

        if use_time:
            date_time = '[%s] ' % strftime(Output.date_format, localtime())

        message_type = '[%s]' % colored(result[0], result[1], attrs=result[2])
        message_result = '%s%s %s' % (message_type, date_time, message)

        if Output.log_file:
            message_result_text = '[%s]%s %s' % (result[0], date_time, message)
            Output.file_resource.write(message_result_text + '\n')

        if ret:
            return message_result

        print(message_result)

    @staticmethod
    def log(message: str):
        if Output.quiet:
            return

        if Output.logging:
            Output.do(message, result=OutputResult.Log)
