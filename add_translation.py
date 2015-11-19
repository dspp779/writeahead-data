#!/usr/bin/env python 
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import time
import sys
from microsofttranslator import Translator
translator = Translator('pengyu', 'AYNUzxXsrbJAHEnC225cwSRnX1vinlqbuh3ndUozVkA=')
# translator = Translator('pengyu2', '4ZmrcZmhQuau5QiiNaBa83pkCspSKjkcZ6jIuCK1sEw=')
to_languages = [u'en', u'zh-tw', u'ja']
def try_translate(sent, lang):
    while True:
        try:
            return translator.translate(sent, lang)
        except Exception, e:

            sys.stderr.write(str(e)+'\n')
            time.sleep(3)

if __name__ == '__main__':
    # gs = goslate.Goslate()
    table = json.load(open('patterns.json'))
    for key, val in table.iteritems():
        for pat in val[1:]:
            for col in pat[2]:
                sent = col[0].replace(u'[', u'').replace(u']', u'')
                sents = [ (u'en', col[0].replace(u'[', u'').replace(u']', u'')) ]
                sents += [ (lang.split('-')[0], try_translate(sent, lang)) for lang in to_languages[1:] ]
                sents = dict(sents)
                col += [ sents ]
        # print list(val)
        # break
    try:
        json.dump(table,open('new_patterns.json','w'))
    except:
        print table
