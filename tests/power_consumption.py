#!/usr/bin/env python
import subprocess as subp
import yaml
from avocado import Test
from internet_utils import InternetUtils

class PowerConsumption(Test):
    def test(self):
        # has temp self arg ** This line should be changed when
        #                      implemented in Benjamins env **
        powerdata = InternetUtils.load_yaml(self, "data/power_data.yaml")
        
    def 
