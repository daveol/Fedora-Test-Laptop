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
    with open(path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            test_class.log.debug(exc)

