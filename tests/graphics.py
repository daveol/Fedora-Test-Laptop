import re
import os

import subprocess

from avocado import Test

from fed_laptoptest.hwinfo import HWinfo


def _get_glxinfo(text):
    """
    Pull the relavant device and venodor strings out of the glxinfo output
    """
    # Regex for device/vendor sets
    regex = r"\s+(Device|Vendor):\s+(.+)\s+\((0x[a-f0-9]+)\)"

    # Dictonary for results
    result = {}

    # Search for strings
    matches = re.finditer(regex, text)

    for match in matches:
        result[match.group(1).lower()] = match.group(2)

    return result


class StandardGraphics(Test):
    """
    This tests the if standard graphics card get's utilized by OpenGL

    This executes glxinfo with DRI_PRIME=0 and looks if the vendor and the
    dveice match that of the hwinfo database
    """
    def setUp(self):
        """
        Setup the Standard graphics data
        """

        self.hwinfo = HWinfo()

        try:
            device = self.hwinfo.graphics['standard']['device']
            vendor = self.hwinfo.graphics['standard']['vendor']
            self.log.debug(
                'checking for graphics device "%s" from vendor "%s"',
                device,
                vendor
            )
        except:
            self.skip('Required graphics card info not found')

    def test(self):
        """
        Execute glxinfo and test the results
        """

        # Create environment variables
        env = {
            'DRI_PRIME': '0'
        }

        # Place existing stuff in there
        env.update(os.environ)

        # This is the wrong way, and thus only works for logged in users with
        # the display variables
        #
        # TODO: use fed_laptoptest.session.Session.spawn_process to fix above?
        output = subprocess.call(['glxinfo'], env=env)

        results = _get_glxinfo(output)

        for key, value in results.iteritems():
            # Get the correct value
            db_value = self.hwinfo['graphics']['standard'][key]

            # Compare them
            if db_value == value:
                self.fail(
                    'expected to find %s %s but got %s',
                    key,
                    db_value,
                    value
                )


class HybridGraphics(Test):
    """
    This tests the if hybrid graphics card get's utilized by OpenGL

    This executes glxinfo with DRI_PRIME=1 and looks if the vendor and the
    dveice match that of the hwinfo database
    """
    def setUp(self):
        """
        Setup the "Hybrid" graphics data
        """

        self.hwinfo = HWinfo()

        try:
            device = self.hwinfo.graphics['hybrid']['device']
            vendor = self.hwinfo.graphics['hybrid']['vendor']
            self.log.debug(
                'checking for graphics device "%s" from vendor "%s"',
                device,
                vendor
            )
        except:
            self.skip('Required graphics card info not found')

    def test(self):
        """
        Execute glxinfo and test the results
        """

        # Create environment variables
        env = {
            'DRI_PRIME': '1'
        }

        # Place existing stuff in there
        env.update(os.environ)

        # This is the wrong way, and thus only works for logged in users with
        # the display variables
        #
        # TODO: use fed_laptoptest.session.Session.spawn_process to fix above?
        output = subprocess.call(['glxinfo'], env=env)

        results = _get_glxinfo(output)

        for key, value in results.iteritems():
            # Get the correct value
            db_value = self.hwinfo['graphics']['hybrid'][key]

            # Compare them
            if db_value == value:
                self.fail(
                    'expected to find %s %s but got %s',
                    key,
                    db_value,
                    value
                )
