#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re

def check_promo(text):
    """Inspects text and returns an inference of the promotion
    ('success', 'none', 'fail').
    Input:
        text -- UTF-8 text string (required | type: str).
    Output:
        promo -- promotion: 'success', 'none', 'fail' (type: str).

    """

    promo = 'none'
    context_multi = ['reset password', 'password reset', 'forgot password',
                     'forgot my password']
    context_single = ['password', 'pass', 'parole', 'reset']
    promo_multi = ['virtual assistant', 'virtual agent']
    promo_single = ['virtual', 'assistant', 'agent']
    word_pattern = re.compile("(?:[a-zA-Z]+[-–’'`ʼ]?)*[a-zA-Z]+[’'`ʼ]?")
    words = word_pattern.findall(text)
    # Check `context_single`
    for el in context_multi:
        if el in text:
            promo = 'fail'
            break
    if promo == 'none':
        # Check `context_single`
        for el in context_single:
            if el in words:
                promo = 'fail'
                break
    # Check `promo_multi`
    if promo == 'fail':
        for el in promo_multi:
            if el in text:
                promo = 'success'
                break
    # Check `promo_single`
    if promo == 'fail':
        for el in promo_single:
            if el in words:
                promo = 'success'
                break
    return promo
