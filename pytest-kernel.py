from ipykernel.ipkernel import IPythonKernel
from IPython.lib import kernel
import json
from notebook import notebookapp
import os
import urllib.request
from tornado import gen


# The IPythonKernel class is a complete implementation of the Python3 kernel for Jupyter
# To create a clone one just needs to sub-class it
class PythonCloneKernel(IPythonKernel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set flag to check for first call to 'do_execute'
        self.is_first_call = True
        
        # Source: https://stackoverflow.com/a/13055551/2926226
        # Fetch kernel id
        connection_file_path = kernel.get_connection_file()
        connection_file = os.path.basename(connection_file_path)
        self.kernel_id = connection_file.split('-', 1)[1].split('.')[0]

        # Fetch and create sessions url for server
        # Used to fetch the notebook name
        server = next(notebookapp.list_running_servers())      # WARNING: Uses the first server found in the generator
        self.sessions_url = f"{server['url']}api/sessions?token={server['token']}"

    
    def get_notebook_name(self):
        sessions = json.load(urllib.request.urlopen(self.sessions_url))

        for session in sessions:
            if session['kernel']['id'] == self.kernel_id:
                return session['notebook']['path']

    
    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        # We inject ipytest code on either side of the code block to get pytest to work
        # We set the __file__ variable needed by ipytest to run the tests
        # We clean previous tests (from previous blocks)
        PREFIX = f"__file__ = '{self.get_notebook_name()}'\nipytest.clean_tests()"

        # We append the run command at the end
        # -s means show the result of print statements
        # -qq will suppress verbosity (useful for non-test code in which case nothing will show up)
        # -x means stop at the first failed test
        SUFFIX = "ipytest.run('-sqqx')"

        # Inject ipytest commands ONLY if there is a test in code:
        # If ANY of the lines contain the substring 'def test_' we inject ipytest 
        if any(["def test_" in _ for _ in code.splitlines()]):
            code = f"{PREFIX}\n{code}\n{SUFFIX}"

        # In the first call we add the relevant imports before the injected code
        if self.is_first_call:
            self.is_first_call = False
            # We import and optionally configure ipytest
            code = f"import ipytest\n{code}"

        return super().do_execute(code, silent, store_history, user_expressions, allow_stdin)


def log(msg):
    '''Dev utility for logging to tmp file'''

    with open('/tmp/pytest-kernel.log', 'a') as fout:
        fout.write(msg + '\n')
        fout.flush()


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=PythonCloneKernel)
