# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from xmas2016.content.testing import XMAS2016_CONTENT_INTEGRATION_TESTING  # noqa
from xmas2016.content.interfaces import IPlayer

import unittest2 as unittest


class PlayerIntegrationTest(unittest.TestCase):

    layer = XMAS2016_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Player')
        schema = fti.lookupSchema()
        self.assertEqual(IPlayer, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Player')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Player')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IPlayer.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory('Player', 'Player')
        self.assertTrue(
            IPlayer.providedBy(self.portal['Player'])
        )
