# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from xmas2016.content.testing import XMAS2016_CONTENT_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that xmas2016.content is properly installed."""

    layer = XMAS2016_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if xmas2016.content is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'xmas2016.content'))

    def test_browserlayer(self):
        """Test that IXmas2016ContentLayer is registered."""
        from xmas2016.content.interfaces import (
            IXmas2016ContentLayer)
        from plone.browserlayer import utils
        self.assertIn(IXmas2016ContentLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = XMAS2016_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['xmas2016.content'])

    def test_product_uninstalled(self):
        """Test if xmas2016.content is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'xmas2016.content'))

    def test_browserlayer_removed(self):
        """Test that IXmas2016ContentLayer is removed."""
        from xmas2016.content.interfaces import IXmas2016ContentLayer
        from plone.browserlayer import utils
        self.assertNotIn(IXmas2016ContentLayer, utils.registered_layers())
