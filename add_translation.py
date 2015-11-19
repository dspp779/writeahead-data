#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import json
import goslate

to_languages = [u'en', u'zh-tw', u'ja']

if __name__ == '__main__':
    gs = goslate.Goslate()
    table = json.load(open('/datum/patterns.json'))
    for key, val in table.iteritems():
        for pat in val[1:]:
            for col in pat[2]:
                sent = col[0].replace(u'[', u'').replace(u']', u'')
                sents = [ (u'en', col[0].replace(u'[', u'').replace(u']', u'')) ]
                sents += [ (lang.split('-')[0], gs.translate(sent, lang)) for lang in to_languages[1:] ]
                sents = dict(sents)
                col += [ sents ]
        print list(val)
        break
