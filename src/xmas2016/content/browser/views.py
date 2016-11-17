# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
from DateTime import DateTime
from Products.CMFPlone.utils import safe_unicode
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
import hashlib
import logging

logger = logging.getLogger("Xmas2016.content")

class IndexView(BrowserView):
    """ Index View
    """
    index = ViewPageTemplateFile("template/index_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
        catalog = context.portal_catalog
        portal = api.portal.get()
        alsoProvides(request, IDisableCSRFProtection)

        sha = request.form.get('sha')
        order = request.form.get('order')
        if sha  and order:
            pass
        else:
            self.allowPlay = False
            return self.index()

        hashkey = portal['resource']['player'].hashkey
        shaValue = hashlib.sha256('%s%s' % (hashkey, order)).hexdigest().upper()
        if shaValue == sha:
            self.allowPlay = True
        else:
            self.allowPlay = False

        return self.index()


class GameView(BrowserView):
    """ Game View
    """
    index = ViewPageTemplateFile("template/game_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
        catalog = context.portal_catalog
        portal = api.portal.get()
        alsoProvides(request, IDisableCSRFProtection)

        return self.index()


class PrizeView(BrowserView):
    """ Prize View
    """
    index = ViewPageTemplateFile("template/prize_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
        catalog = context.portal_catalog
        portal = api.portal.get()
        alsoProvides(request, IDisableCSRFProtection)

        return self.index()

