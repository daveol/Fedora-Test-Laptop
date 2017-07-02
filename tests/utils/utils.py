#!/usr/bin/env python

# Copyright 2017 Nick Dekker, Marthe Veldhuis.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see LICENSE.txt.

import yaml
from avocado.core import settings
import os.path

def get_data_dir():
    # Try relative to this in case it is not properly installed
    _path = os.path.join(os.path.dirname(__file__), '..', 'data')
    if not os.path.isdir(_path):
        _path = settings.settings.get_value('datadir.paths', 'data_dir', 'path')
    return _path

def load_yaml(test_class, path):
    """
    Tries to open and load the yaml file referenced, skips the test when
    the yaml file cannot be opened or loaded for some reason, e.g. when
    the file is not found.
    
    :param path: The path where the yaml file is located
    :param test_class: The class to skip when the yaml cannot be loaded
    :return: Yaml file as a stream
    
    """
    try:
        with open(path, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as ex:
                test_class.skip("Yaml file could not be loaded")
    except IOError as exc:
        test_class.skip("Yaml file could not be opened")
