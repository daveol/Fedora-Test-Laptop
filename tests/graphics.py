import os

from avocado import main
from avocado.core import exceptions

from fed_laptoptest.hwinfo import HWinfo
from fed_laptoptest.test import SessionTest


def _get_hwaccell(DRI_PRIME=0):
    """
    Execute gnome-session-check-accelerated function
    """

    # Set the DRI_PRIME enviroment variable
    os.putenv('DRI_PRIME', str(DRI_PRIME))

    # Then execute and return
    return os.execl('/usr/libexec/gnome-session-check-accelerated', 'gnome-session-check-accelerated')


class StandardGraphics(SessionTest):
    """
    This tests the if standard graphics card get's utilized by OpenGL

    This executes gnome-session-check-accellerated with DRI_PRIME=0 and looks
    if the device matches that in the hwinfo database

    :avocado: enable
    :avocado: tags=manual
    """

    def setUp(self):
        """
        Setup the Standard graphics data & test for executables
        """

        if not os.path.exists('/usr/libexec/gnome-session-check-accelerated'):
            self.skip('gnome-session-check-accellerated not found')

        self.hwinfo = HWinfo()

        try:
            device = self.hwinfo.graphics['standard']['device']
            self.log.debug(
                'checking for graphics device "%s"',
                device
            )
            self.no_data = False
        except:
            self.no_data = True

        SessionTest.setUp(self)

    def test(self):
        """
        Execute gnome-session-check-accelerated and test the results
        """

        proc, output = self.session.spawn_subprocess(
            lambda: _get_hwaccell(DRI_PRIME=0)
        )

        device = ""

        while proc.is_alive():
            device += os.read(output, 1000)

        if proc.exitcode != 0:
            self.fail(
                'gnome-session-check-accellerated returned with error code %s',
                str(proc.exitcode)
            )

        if not self.no_data:
            # Get the correct value
            db_value = self.hwinfo['graphics']['standard']['device']

            # Compare them
            if db_value == device:
                self.fail(
                    'expected to find %s but got %s',
                    (db_value, device)
                )


class HybridGraphics(SessionTest):
    """
    This tests the if hybrid graphics card get's utilized by OpenGL

    This executes gnome-session-check-accellerated with DRI_PRIME=1 and looks
    if the device matches that in the hwinfo database

    :avocado: enable
    :avocado: tags=manual
    """

    def setUp(self):
        """
        Setup the "Hybrid" graphics data
        """

        if not os.path.exists('/usr/libexec/gnome-session-check-accelerated'):
            self.skip('gnome-session-check-accellerated not found')

        self.hwinfo = HWinfo()

        try:
            device = self.hwinfo.graphics['hybrid']['device']
            self.log.debug(
                'checking for graphics device "%s"',
                device
            )
        except:
            self.skip('Required graphics card info not found')

        SessionTest.setUp(self)

    def test(self):
        """
        Execute gnome-session-check-accellerated and test the output value
        """

        proc, output = self.session.spawn_subprocess(
            lambda: _get_hwaccell(DRI_PRIME=1)
        )

        device = ""

        while proc.is_alive():
            device += os.read(output, 1000)

        if proc.exitcode != 0:
            self.fail(
                'gnome-session-check-accellerated returned with error code %i',
                proc.exitcode
            )

        # Get the correct value
        db_value = self.hwinfo['graphics']['hybrid']['device']

        # Compare them
        if db_value == device:
            self.fail(
                'expected to find %s but got %s',
                (db_value, device)
            )

if __name__ == "__main__":
    main()
