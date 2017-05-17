#!/usr/bin/env python

import os
import sys
import yaml
from . import utils

DMI_ID_PATH='/sys/class/dmi/id/'



def _merge_dict(d1, d2):
    for k, v in d2.iteritems():
        if k not in d1:
            d1[k] = v
            continue

        if isinstance(v, dict):
            _merge_dict(d1[k], v)
        else:
            d1[k] = v

class HWinfo(object):

    # Ordered by how specific they are
    DMI_ID = ['sys_vendor', 'board_vendor', 'chassis_vendor', 'chassis_type',
              'product_version', 'board_name', 'chassis_version',
              'product_name']

    def __init__(self, load=True):
        self.dmi_id = self.dmi_load()

        if load:
            matches = []
            for hw in _hw:
                score = self._dmi_match(hw)
                if not score:
                    continue
                matches.append((score, hw))

            matches.sort()
            matches = [m[1] for m in matches]
            for m in matches:
                self._merge_info(m)

    def _merge_info(self, m):
        for k in m.iterkeys():
            if k == 'dmi_id':
                continue

            if hasattr(self, k):
                print(k)
                _merge_dict(getattr(self, k), m[k])
            else:
                setattr(self, k, m[k])

    def _dmi_match(self, hwinfo):
        # Returns whether there is a match and how good it is for ordering
        if 'dmi_id' not in hwinfo:
            return False
        score = 0

        for k, v in hwinfo['dmi_id'].iteritems():
            matches = False
            if isinstance(v, list):
                if self.dmi_id[k] in v:
                    matches = True
            else:
                if self.dmi_id[k] == v:
                    matches = True

            if not matches:
                return False

            score += 2**self.DMI_ID.index(k)

        return score

    def dmi_load(self):
        res = {}
        for k in self.DMI_ID:
            res[k] = open(os.path.join(DMI_ID_PATH, k)).read().strip()

        return res

    def dump(self, stream=None):
        res = {}
        for k in self.__dict__.iterkeys():
            if k.startswith('_'):
                continue
            res[k] = getattr(self, k)

        return yaml.dump(res, stream, default_flow_style=False)

    def __str__(self):
        return self.dump()

_hw = []

# Prefer a local directory with the information
_path = utils.get_data_dir()

for root, dirs, files in os.walk(_path):
    for f in files:
        if not f.endswith('.yaml'):
            continue

        p = os.path.join(root, f)

        try:
            _hw.append(yaml.load(open(p)))
        except Exception, e:
            sys.stderr.write("Could not load file %s:\n" % p)
            sys.stderr.write(str(e))
            sys.stderr.write('\n----\n')

if __name__ == "__main__":
    hw = HWinfo()
    print(hw)

