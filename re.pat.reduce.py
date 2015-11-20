#!/usr/bin/env python 
# -*- coding: utf-8 -*-
from __future__ import division

import sys, fileinput
import operator
import json

from collections import Counter, defaultdict, OrderedDict
from itertools import groupby, imap, islice
from math import sqrt

# pv citeseerx.sents.tagged.h.10000.txt | sh local_mapreduce.sh 0.8m 10 'python col.map.py' 'python col.reduce.py' result_dir


class OrderedDefaultDict(OrderedDict):
    def __init__(self, default_factory=None, *args, **kwargs):
        super(OrderedDefaultDict, self).__init__(*args, **kwargs)
        self.default_factory = default_factory
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        val = self[key] = self.default_factory()
        return val

k0 = 1
k1 = 1
U0 = 10
minCount = 10

class wordPat(Counter):
    def __init__(self):
        self.default_factory = Counter

    def __repr__(self):
        #tail = ', ...' if len(self) > 3 else ''
        items = ', \n    '.join(map(str, self.iteritems()))
        return '{}(freq = {}, avg_freq = {}, dev = {}, \n \n)'.format(self.__class__.__name__, self.freq, self.avg_freq, self.dev, items)

    def calc_metrics(self):
        self.freq = sum(self.values())
        self.avg_freq = self.freq/len(self)
        self.dev = sqrt(sum((xfreq - self.avg_freq)**2 for xfreq in self.values() )/len(self))

    def gen_goodpat(self):
        if self.freq == 0 or self.dev == 0: return
        for pat, count in self.most_common():
            if (count - self.avg_freq) / self.dev <= k0:
                break
            if count <= minCount:
                break
            yield pat, count
    

#difficulty:N	difficulty about something	difficulty about learning	difficulty about multiagent learning	1	4	8
def line_to_headword(x):
    return x.strip().split('\t')[0].decode('unicode_escape')
    
def line_to_pat(x):
    return x.strip().split('\t')[1].decode('unicode_escape')

if __name__ == '__main__':
    table = {}
    for headword, lines in groupby(fileinput.input(), key=line_to_headword):
        lines = sorted(lines)

        patInstances = { pat: list(instances) for pat, instances in groupby(lines, key=line_to_pat) }
        patCounts = { pat: len(instances) for pat, instances in patInstances.iteritems() }

        patterns = wordPat()
        patterns.update( patCounts )
        patterns.calc_metrics()

        goodPats = list(patterns.gen_goodpat())
        
        for pat, count in goodPats:
            print ('%s\t%s\t%d' % (headword, pat, count)).encode('utf-8')

