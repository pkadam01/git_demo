from lattehhpel import *


class FakePEL(HHPEL):

    def send_command(self, command_string):
        return None
