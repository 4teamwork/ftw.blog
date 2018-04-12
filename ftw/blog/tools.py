# -*- coding: utf-8 -*-
from Products.CMFPlone.i18nl10n import monthname_msgid
from zope.i18n import translate


def abbmonth(time):
    """Return abbreviated internationalized month name
    """
    return monthname_msgid(time.strftime("%m"))


def zLocalizedTime(request, time, long_format=False):
    """Convert time to localized time
    """
    month_msgid = abbmonth(time)
    month = translate(month_msgid, domain='plonelocales',
                      context=request)

    return u"%s" % (month)
