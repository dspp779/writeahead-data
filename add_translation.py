#!/usr/bin/env python 
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import time
import sys
from microsofttranslator import Translator

to_languages = [u'en', u'zh-tw', u'ja']

if __name__ == '__main__':
    table         = json.load(open(sys.argv[1]))
    client_id     = sys.argv[2]
    client_secret = sys.argv[3]
    translator    = Translator(client_id, client_secret)
    for key, val in table.iteritems():
        for pat in val[1:]:
            for col in pat[2]:
                if type(col[-1]) != dict:
                    sent = col[0].replace(u'[', u'').replace(u']', u'')
                    sents = [ (u'en', col[0].replace(u'[', u'').replace(u']', u'')) ]
                    try:
                        sents += [ (lang.split('-')[0], translator.translate(sent, lang)) for lang in to_languages[1:] ]
                    except Exception, e:
                        done = sum([ 1 for key, val in table.iteritems() for pat in val[1:] for col in pat[2] if type(col[-1])==dict])
                        total = sum([ 1 for key, val in table.iteritems() for pat in val[1:] for col in pat[2]])
                        sys.stderr.write(str(e)+'\n')
                        sys.stderr.write('total:{} done:{}\n'.format(total,done))
                        json.dump(table,open('new_patterns.json','w'))
                        sys.exit(0)
                    sents = dict(sents)
                    col += [ sents ]
        # print list(val)
        # break
    try:
        json.dump(table,open('new_patterns.json','w'))
        print 'done!!!!!'
    except:
        print table
