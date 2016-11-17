# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from xmas2016.content import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IXmas2016ContentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPlayer(Interface):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    player = schema.Text(
        title=_(u"Players, JSON format"),
        required=False,
    )

    awarder = schema.Text(
        title=_(u"Awarder, JSON format"),
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

    hashkey = schema.TextLine(
        title=_(u"Hash Key"),
        required=True,
    )
