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
import json
import logging

logger = logging.getLogger("Xmas2016.content")


class BaseMethod(BrowserView):

    def paraString(self):
        context = self.context
        request = self.request

        if not request.form:
            return ''

        paraStr = ''
        for para in request.form:
            paraStr += '%s=%s&' % (para, request.form.get(para))

        return paraStr


    def alreadyPlayed(self, order):
        context = self.context
        request = self.request
        portal = api.portal.get()
        alsoProvides(request, IDisableCSRFProtection)

        player = json.loads(portal['resource']['player'].player)
        if order in player:
            return True
        else:
            return False


    def checkPara(self, sha, order):
        context = self.context
        request = self.request
        portal = api.portal.get()
        alsoProvides(request, IDisableCSRFProtection)

        if sha  and order:
            pass
        else:
            return False

        hashkey = portal['resource']['player'].hashkey
        shaValue = hashlib.sha256('%s%s' % (hashkey, order)).hexdigest().upper()
        if shaValue == sha:
            return True
        else:
            return False


class IndexView(BaseMethod):
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

        self.allowPlay = self.checkPara(sha, order) and not self.alreadyPlayed(order)

        return self.index()


class GameView(BaseMethod):
    """ Game View
    """
    index = ViewPageTemplateFile("template/game_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
        catalog = context.portal_catalog
        portal = api.portal.get()
        alsoProvides(request, IDisableCSRFProtection)

        sha = request.form.get('sha')
        order = request.form.get('order')

        self.allowPlay = self.checkPara(sha, order) and not self.alreadyPlayed(order)
        if not self.allowPlay:
            request.response.redirect(portal.absolute_url())
            return

        return self.index()


class PrizeView(BaseMethod):
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


class AwardResult(BaseMethod):

    """ 遊戲結果寫入"""
    def __call__(self):
        context = self.context
        request = self.request
        catalog = context.portal_catalog
        portal = api.portal.get()
        alsoProvides(request, IDisableCSRFProtection)

        return

