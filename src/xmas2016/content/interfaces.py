# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from xmas2016.content import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.directives import dexterity


class IXmas2016ContentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPlayer(Interface):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    dexterity.write_permission(played='cmf.ManagePortal')
    played = schema.Text(
        title=_(u"Played players, JSON format"),
        default=u"{}",
        required=False,
    )

    awardRate = schema.Float(
        title=_(u"Award Rate"),
        default=0.01,
        required=True,
    )

    maxAward_100 = schema.Int(
        title=_(u"Max Award 100"),
        default=300,
        required=True,
    )

    dailyAward_100 = schema.Int(
        title=_(u"Daily Award 100"),
        default=10,
        required=True,
    )

    dexterity.write_permission(awarder_100='cmf.ManagePortal')
    awarder_100 = schema.Text(
        title=_(u"Awarder 100, JSON format"),
        default=u"{}",
        required=False,
    )

    maxAward_50 = schema.Int(
        title=_(u"Max Award 50"),
        default=1500,
        required=True,
    )

    dailyAward_50 = schema.Int(
        title=_(u"Daily Award 50"),
        default=50,
        required=True,
    )

    dexterity.write_permission(awarder_50='cmf.ManagePortal')
    awarder_50 = schema.Text(
        title=_(u"Awarder 50, JSON format"),
        default=u"{}",
        required=False,
    )

    dateStart = schema.Date(
        title=_("Date Start"),
        required=True,
    )

    dateEnd = schema.Date(
        title=_("Date End"),
        required=True,
    )

    dexterity.write_permission(hashkey='cmf.ManagePortal')
    hashkey = schema.TextLine(
        title=_(u"Hash Key"),
        required=True,
    )
