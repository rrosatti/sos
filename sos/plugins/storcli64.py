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

        self.add_cmd_output([
                            "storcli64 show all",
                            "storcli64 -v"])
        
        for i in range(0, num_ctrls):
            # /cx /eall show commands
            self.add_cmd_output([
                                "storcli64 /c%d /eall show status" % i,
                                "storcli64 /c%d /eall show phyerrorcounters" % i])

            # /cx /eall /sall show commands
            eall_dall_show = ["all", "health", "copyback", "phyerrorcounters", "initialization", "securitykey keyid", "erase"]
            for op in eall_dall_show:
                self.add_cmd_output("storcli64 /c%d /eall /sall show %s" % (i, op))

            # /cx /vall show commands
            # idea: check if VDs are configured or not
            vall_show = ["all", "expansion", "init", "cc", "erase", "migrate", "bgi", "autobgi", "trim", "BBMT"]
            for op in vall_show:
                self.add_cmd_output("storcli64 /c%d /vall show %s" % (i, op))

            # /cx /bbu show commands
            # idea: same as above (check if battery is absent)
            bbu_show = ["all", "status", "properties", "learn", "modes"]
            for op in bbu_show:
                self.add_cmd_output("storcli64 /c%d /bbu show %s" % (i, op))

            # other commands
            # idea: check cd (checkvault) separetely
            #       same for dall (diskgroup)
            self.add_cmd_output([
                                "storcli64 /c%d /dall show all" % i,
                                "storcli64 /c%d /dall show cachecade" % i,
                                "storcli64 /c%d /dall show mirror" % i,
                                "storcli64 /c%d /fall show all" % i,
                                "storcli64 /c%d /pall show all" % i,
                                "storcli64 /c%d /cv show all" % i,
                                "storcli64 /c%d /cv show status" % i,
                                "storcli64 /c%d /cv show learn" % i,
                                "storcli64 /c%d /mall show" % i])

            # /cx show commands
            cx_show = ["events", "eventloginfo", "health", "termlog", 
                    "sesmonitoring", "failpdonsmarterror", "freespace",
                    "fshinting", "cc", "ocr", "all", "preservedcache",
                    "bootdrive", "bootwithpinnedcache", "activityforlocate",
                    "copyback", "jbod", "autorebuild", "autopdcache",
                    "cachebypass", "usefdeonlyencrypt",
                    "prcorrectunconfiguredareas", "batterywarning",
                    "abortcconerror", "ncq", "configautobalance",
                    "maintainpdfailhistory", "restorehotspare", "bios",
                    "alarm", "foreignautoimport", "directpdmapping",
                    "rebuildrate", "loadbalancemode", "eghs", "cacheflushint",
                    "prrate", "ccrate", "bgirate", "dpm", "sgpioforce",
                    "migraterate", "spinupdrivecount", "wbsupport",
                    "spinupdelay", "coercion", "limitMaxRateSATA",
                    "HDDThermalPollInterval", "SSDThermalPollInterval",
                    "smartpollinterval", "eccbucketsize", "eccbucketleakrate",
                    "backplane", "perfmode", "perfmodevalues", "pi", "time",
                    "ds", "safeid", "rehostinfo", "pci", "ASO",
                    "flush cachecade", "securitykey keyid", "patrolRead",
                    "powermonitoringinfo", "ldlimit", "badblocks",
                    "maintenance", "personality", "jbodwritecache",
                    "immediateio", "driveactivityled", "largeiosupport",
                    "pdfailevents", "pdfaileventoptions", "AliLog",
                    "flushwriteverify", "largeQD"]
            for op in cx_show:
                self.add_cmd_output("storcli64 /c%d show %s" % (i, op))
