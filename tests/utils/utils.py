import yaml

def load_yaml(test_class, path):
    with open(path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            test_class.log.debug(exc)

