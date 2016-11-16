# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import xmas2016.content


class Xmas2016ContentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=xmas2016.content)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'xmas2016.content:default')


XMAS2016_CONTENT_FIXTURE = Xmas2016ContentLayer()


XMAS2016_CONTENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(XMAS2016_CONTENT_FIXTURE,),
    name='Xmas2016ContentLayer:IntegrationTesting'
)


XMAS2016_CONTENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(XMAS2016_CONTENT_FIXTURE,),
    name='Xmas2016ContentLayer:FunctionalTesting'
)


XMAS2016_CONTENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        XMAS2016_CONTENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='Xmas2016ContentLayer:AcceptanceTesting'
)
