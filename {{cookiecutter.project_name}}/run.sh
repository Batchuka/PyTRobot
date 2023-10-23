#!/bin/bash

if [ "$xvfb" = "true" ]; then
    xvfb-run -a python3 -m {{cookiecutter.project_name}}.main
else
    python3 -m {{cookiecutter.project_name}}.main
fi