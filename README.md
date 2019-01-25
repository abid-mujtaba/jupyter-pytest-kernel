## pytest kernel for Jupyter Notebooks

This is a thin wrapper around the standard ipython3 kernel and makes use of the existing [ipytest](https://github.com/chmp/ipytest) module to provide transparent execution of pytest code in Jupyter Notebooks.

### Reasoning

Jupyter Notebooks are a fantastic teaching resource, especially for teaching Python. I have felt its lack when I have taught `pytest` and desired the ability to use Jupyter to show and execute pytest examples.

Fortunately [ipytest](https://github.com/chmp/ipytest) has already done all the heavy-lifting and all that remains was to implement this thin wrapper to create a pytest kernel.

### Caution

This is a work in progress. In its current state this will only work if the `jupyter notebook` command is run from the same folder as the `pytest-kernel.py` file.

### Future

The goal, once completed, is to create a pip package that will make installation painless.

### Example

TODO: Add example notebook.
