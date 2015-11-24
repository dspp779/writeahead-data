#!/usr/bin/env python 
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import time
import sys
from microsofttranslator import Translator

# translator = Translator('pengyu2', '4ZmrcZmhQuau5QiiNaBa83pkCspSKjkcZ6jIuCK1sEw=')
to_languages = [u'en', u'zh-tw', u'ja']
# def try_translate(sent, lang):
#     while True:
#         try:
#             return translator.translate(sent, lang)
#         except Exception, e:

#             sys.stderr.write(str(e)+'\n')
#             time.sleep(3)

if __name__ == '__main__':
    client_id     = raw_input('enter your client id:')
    client_secret = raw_input('enter your client secret:')
    translator    = Translator(client_id, client_secret)
    table         = json.load(open('patterns.json'))
    for key, val in table.iteritems():
        for pat in val[1:]:
            for col in pat[2]:
                if type(col[-1]) != dict:
                    sent = col[0].replace(u'[', u'').replace(u']', u'')
                    sents = [ (u'en', col[0].replace(u'[', u'').replace(u']', u'')) ]
                    try:
                        sents += [ (lang.split('-')[0], translator.translate(sent, lang)) for lang in to_languages[1:] ]
                    except Exception, e:
                        sys.stderr.write(str(e)+'\n')
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
