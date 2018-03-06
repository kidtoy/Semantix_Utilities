from AutoDeploy import CreateAndDeploy
import sys
import unittest

class TestMethods(unittest.TestCase):

    # Wrong Cluster/Port
    def testCassandraData(self):
        if CreateAndDeploy.cassandraData('',2132).__len__() != 0:
            sys.exit("testCassandraData Failed")
        else:
            self.assertTrue(True)
        self.assertFalse(False)

    def testGetWhitelist(self):
        if CreateAndDeploy.getWhitelist('',2132,"bradesco") == True:
            sys.exit("testGetWhitelist Failed")
        else:
            self.assertTrue(True)
        self.assertFalse(False)


    def testGetTenantGuid(self):
        if type(CreateAndDeploy.getTenantGUID()) is not str :
            sys.exit("testGetTenantGuid Failed")
        else:
            self.assertTrue(True)
        self.assertFalse(False)


    def testGetDevices(self):
        if type(CreateAndDeploy.getDevices()) is not list:
            sys.exit("testGetDevices Failed")
        else:
            self.assertTrue(True)
        self.assertFalse(False)


    def testCreateSession(self):
        # Test Wrong Values
        with self.assertRaises(Exception):
            CreateAndDeploy.createSession('20d1w0uda0u201u231u20d', [{'uuid':'sicxi'}, {'uuid':'dsacx'}])
        # Test Empty Values
        with self.assertRaises(KeyError):
            CreateAndDeploy.createSession('', [{}, {}])


    def testUniteData(self):
        # Test Empty Values
        self.assertTrue(CreateAndDeploy.uniteData([], []).__len__() == 0)

        # Wrong Values
        with self.assertRaises(KeyError):
            CreateAndDeploy.uniteData([{"23dsa": 21}], [{"dasxcz": "312dsa"}])


    def testGetSessions(self):
        # Wrong Value
        self.assertTrue(CreateAndDeploy.getSessions("ac918279x") is None)
        # Empty Value
        self.assertTrue(CreateAndDeploy.getSessions("") is None)


    def testDeleteSession(self):
        # Wrong TenantGuid
        self.assertTrue(CreateAndDeploy.deleteSession("32seacxc231","dsac133") == 502)

        # Empty Session
        self.assertTrue(CreateAndDeploy.deleteSession(CreateAndDeploy.getTenantGUID(), "") == 405)

        # Wrong Session
        self.assertTrue(CreateAndDeploy.deleteSession(CreateAndDeploy.getTenantGUID(), "231wdsd") == 404)


    def testSendFileSession(self):

        # Wrong TenantGuid
        self.assertTrue(CreateAndDeploy.sendFileSession("", "231wdsd", "9999","bradesco") == 502)

        # Wrong Branch (File doesn't exists)
        self.assertTrue(CreateAndDeploy.sendFileSession(CreateAndDeploy.getTenantGUID(), "231wdsd", "99","bradesco") is False)

        # No Session Available
        self.assertTrue(CreateAndDeploy.sendFileSession(CreateAndDeploy.getTenantGUID(), "231wdsd", "9999","bradesco") == 404)


    def testExecuteSession(self):

        # Wrong TenantGuid
        self.assertTrue(CreateAndDeploy.executeSession("32seacxc231","dsac133") == 502)

        # Empty Session
        self.assertTrue(CreateAndDeploy.executeSession(CreateAndDeploy.getTenantGUID(), "") == 404)

        # Wrong Session
        self.assertTrue(CreateAndDeploy.executeSession(CreateAndDeploy.getTenantGUID(), "231wdsd") == 404)


    def testCleanSessions(self):
        #Wrong TenantGuid
        with self.assertRaises(TypeError):
            CreateAndDeploy.cleanSessions("321d123")

        #Empty TenantGuid
        with self.assertRaises(TypeError):
            CreateAndDeploy.cleanSessions("")


if __name__ == '__main__':
    unittest.main()

