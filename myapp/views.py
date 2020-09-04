# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)


def index(request):
    logger.debug('test 1')

    # logging to the root logger accidentally (logging should be logger)
    # this configures the root logger automatically!
    logging.debug('test 2')

    return render(request, 'example.html')
