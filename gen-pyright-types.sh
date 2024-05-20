#!/bin/bash

source venv/bin/activate

export PYTHONPATH="$PWD/bin"

pybind11-stubgen -o src steanography

deactivate
