# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


from sos.plugins import Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin
import os



class Storcli64(Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin):

    plugin_name = "storcli"
    packages = ('storcli64',)

    def get_num_ctrls(self, cmd_ctrlcount_out):
        """ Recieves the output from 'storcli64 show ctrlcount' and return the
        controller count"""

        for line in cmd_ctrlcount_out.splitlines():
            if "Controller Count" in line:
                return line.split()[3]
                break
            return 1

    def setup(self):
        # get controllers count
        cmd_ctrlcount = self.call_ext_prog("storcli64 show ctrlcount")
        if cmd_ctrlcount['status'] == 0:
            num_ctrls = self.get_num_ctrls(cmd_ctrlcount['output'])

        print(num_ctrls)

