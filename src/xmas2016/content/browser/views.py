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
import random
import logging
import urllib2

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

        played = json.loads(portal['resource']['player'].played)
        if order in played:
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

        sha = request.form.get('sha')
        order = request.form.get('order')

        self.allowPlay = self.checkPara(sha, order) and not self.alreadyPlayed(order)
        if not self.allowPlay:
            request.response.redirect(portal.absolute_url())
            return

        player = portal['resource']['player']
        played = json.loads(player.played)
        awardRate = player.awardRate
        maxAward_100 = player.maxAward_100
        dailyAward_100 = player.dailyAward_100
        awarder_100 = json.loads(player.awarder_100)
        maxAward_50 = player.maxAward_50
        dailyAward_50 = player.dailyAward_50
        awarder_50 = json.loads(player.awarder_50)
        dateStart = player.dateStart
        dateEnd = player.dateEnd
        hashkey = player.hashkey

        pastDay = int(DateTime() - DateTime(dateStart.isoformat()) + 1)
        quota_100 = True if len(awarder_100) < dailyAward_100 * pastDay else False
        quota_50 = True if len(awarder_50) < dailyAward_50 * pastDay else False

        if not quota_100 and quota_50:
            awardRate = 0

        hasAward = random.randrange(1,100) <= awardRate*100
        if hasAward: # 有中獎
            if quota_100 and quota_50:
                self.awardItem = random.choice([100, 50])
            elif quota_100:
                self.awardItem = 100
            else:
                self.awardItem = 50
        else:
            self.awardItem = 0

        playTime = DateTime().strftime('%c')
        remoteIP = request.get('HTTP_X_FORWARDED_FOR')

        played[order] = (playTime, remoteIP)
        player.played = json.dumps(played)
        if self.awardItem == 50:
            awarder_50[order] = (playTime, remoteIP)
            player.awarder_50 = json.dumps(awarder_50)
        elif self.awardItem == 100:
            awarder_100[order] = (playTime, remoteIP)
            player.awarder_100 = json.dumps(awarder_100)

        callBack = 'http://wonder.ielife.net/Xmas2016-2.asp?sha=%s&order=%s&result=%s' % (sha, order, self.awardItem)

        try:
            urllib2.urlopen(callBack)
            logger.info(callBack)
        except:
            with open('/home/andyfang51/tmp/holdURL', 'a') as file:
                file.write('%s\n' % callBack)

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


class PlayerView(BaseMethod):
    """ Player View
    """

    index = ViewPageTemplateFile("template/player_view.pt")

    def __call__(self):
        context = self.context
        self.played = json.loads(context.played)
        self.awarder_100 = json.loads(context.awarder_100)
        self.awarder_50 = json.loads(context.awarder_50)


        return self.index()

