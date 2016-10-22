from kernel.output import Output, OutputResult
from io import StringIO
import sys

# @url: http://stackoverflow.com/a/16571630
# STDOUT capture class
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout

def test_main_output_func():
    with Capturing() as output:
        Output.do("Test")

    assert output._stringio.getvalue().find("Test") != -1
    assert not output._stringio.getvalue().find("Nonexistent") != -1

    output_result_types = [
        OutputResult.OK, OutputResult.Fail, OutputResult.Info,
        OutputResult.Warn, OutputResult.Error, OutputResult.Log
    ]

    for R in output_result_types:
        with Capturing() as output:
            Output.do("UnitTestCase test")

        assert output._stringio.getvalue().find("UnitTestCase") != -1
        assert not output._stringio.getvalue().find("Someothervalue") != -1
