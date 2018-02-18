import unittest
import datetime

import ui.snap as snap

class TestUISnap(unittest.TestCase):

    def test_find_cmd(self):
        r = snap.find_cmd("konstructs-client")
        self.assertEqual(len(r), 1, "Expected one result")
        self.assertEqual(r[0].split()[0], "konstructs-client", "Expected konstructs-client")

    def test_find(self):
        r = snap.find("konstructs-client")
        for l in r:
            self.assertEqual(l.name, "konstructs-client", "Expected konstructs-client")

    def test_update_result(self):
        """ This test assumes that konstructs-client is installed """
        r = snap.find("konstructs-client")
        for l in r:
            ur = snap.update_result(l)
            self.assertEqual(ur.summary, "A voxel based game client")
            self.assertEqual(ur.description, ("An open source Infiniminer/Minecraft "
                                              "inspired multiplayer game."))
            self.assertEqual(ur.publisher, "nsg")
            self.assertEqual(ur.contact, "https://github.com/konstructs/client/issues")
            self.assertEqual(ur.snap_id, "vz0NCdgBzBeFaDlSVYCv7zC08ikS6ImI")
            self.assertEqual(ur.commands, ['konstructs-client'])
            self.assertEqual(ur.tracking, "stable")
            self.assertIs(type(ur.refreshed), datetime.datetime)

            i = ur.installed
            self.assertIs(type(i), dict)
            self.assertTrue(i.get("version"))
            self.assertTrue(i.get("rev"))
            self.assertTrue(i.get("size"))

            c = ur.channels
            self.assertIs(type(c), dict)
            self.assertTrue(c.get("stable"))
            self.assertTrue(c.get("edge"))
            self.assertIs(type(c['stable']), dict)
            self.assertIs(type(c['edge']), dict)
            self.assertTrue(c['edge'].get("version"))
            self.assertTrue(c['edge'].get("rev"))
            self.assertTrue(c['edge'].get("size"))

if __name__ == '__main__':
    unittest.main()
