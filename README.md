# datasette-chatgpt-plugin

[![PyPI](https://img.shields.io/pypi/v/datasette-chatgpt-plugin.svg)](https://pypi.org/project/datasette-chatgpt-plugin/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-chatgpt-plugin?include_prereleases&label=changelog)](https://github.com/simonw/datasette-chatgpt-plugin/releases)
[![Tests](https://github.com/simonw/datasette-chatgpt-plugin/workflows/Test/badge.svg)](https://github.com/simonw/datasette-chatgpt-plugin/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-chatgpt-plugin/blob/main/LICENSE)

Turn a Datasette instance into a ChatGPT plugin

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-chatgpt-plugin

## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-chatgpt-plugin
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
