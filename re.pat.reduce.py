#!/usr/bin/env python
from __future__ import division
from collections import Counter, defaultdict
from itertools import groupby, imap
import operator, sys
import fileinput
import json
from itertools import islice
import operator
from math import sqrt

# pv citeseerx.sents.tagged.h.10000.txt | sh local_mapreduce.sh 0.8m 10 'python col.map.py' 'python col.reduce.py' result_dir

from collections import OrderedDict

class OrderedDefaultDict(OrderedDict):
    def __init__(self, default_factory=None, *args, **kwargs):
        super(OrderedDefaultDict, self).__init__(*args, **kwargs)
        self.default_factory = default_factory
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        val = self[key] = self.default_factory()
        return val
table = {}

k0 = 1
k1 = 1
U0 = 10
minCount = 10

class wordPat(Counter):

    def __init__(self):
        self.default_factory = Counter # Collocates

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
        for pat, count in sorted([ (pat, self[pat]) for pat in self if (self[pat] - self.avg_freq) / self.dev > k0 ], 
                        key=lambda x: x[1], reverse=True):
            if count > minCount:
                yield pat, count
    

#difficulty:N	difficulty about something	difficulty about learning	difficulty about multiagent learning	1	4	8
def line_to_word(x):
    return x.strip().split('\t')[0]
    
def line_to_pat(x):
    return x.strip().split('\t')[1]
    
def line_to_col(x):
    return x.strip().split('\t')[2]
    
def line_to_ngram(x):
    return x.strip().split('\t')[3]
    
def line_to_rest(x):
    return '\t'.join(x.strip().split('\t')[2:4])
 
#for word, lines in groupby(input_lines.split('\n'), key=line_to_word): # fileinput.input()
for word, lines in groupby(fileinput.input(), key=line_to_word): # fileinput.input()

    #print 'Handling %s'%word
    #print
    
    patInstances = [ (pat, list(instances)) for pat, instances in groupby(lines, key=line_to_pat) ]
    patCounts = dict([ (pat, len(instances)) for pat, instances in patInstances ])
    patInstances = dict(patInstances)
    
    patterns = wordPat()
    patterns.update( patCounts )
    patterns.calc_metrics()
    goodPats = sorted([ (x, y) for x, y in patterns.gen_goodpat() ], key=lambda x:x[1], reverse=True)
    
    if goodPats:
        #print
        #print '%s (%s)'%(word, sum([ count for _, count in goodPats])) #, goodPats
        #print
        table[word] = [ sum([ count for _, count in goodPats]) ]
    else:
        continue
        
    for pat, count in goodPats[:7]:
        #print '\t*1*%s (%s)'%(pat, count)
        colInstances = [ (col, list(instances)) for col, instances in groupby(patInstances[pat], key=line_to_col) ]
        colCounts = dict([ (col, len(instances)) for col, instances in colInstances ])
        colInstances = dict(colInstances)

        patterns = wordPat()
        patterns.update( colCounts )
        patterns.calc_metrics()
        goodCols = sorted([ (col, count) for col, count in patterns.gen_goodpat() ], key=lambda x:x[1], reverse=True)
        #print '\t*2*%s (%s)'%(pat, patCounts[pat]), goodCols

        if not goodCols:
            #print '\t%s (%s)'%(pat, patCounts[pat]) #, goodCols
            #print
            bestngram = max([ (len(list(instances)), ngram) for ngram, instances in groupby(patInstances[pat], key=line_to_ngram) ])
            #print '\t\t%s (%s, %s)'%(bestngram[1], colCounts[col], bestngram[0])
            table[word] += [ [pat, patCounts[pat], [(bestngram[1], colCounts[col], bestngram[0])]] ]
            #print
            continue
        res = []    
        for col, count in goodCols[:5]:
            bestngram = max([ (len(list(instances)), ngram) for ngram, instances in groupby(colInstances[col], key=line_to_ngram) ])
            #print '\t\t%s (%s, %s)'%(bestngram[1], colCounts[col], bestngram[0])
            res += [(bestngram[1], colCounts[col], bestngram[0])]
        table[word] += [ [pat, patCounts[pat], res] ]
        #print
        
#print table

import json
print json.dumps(table)

'''with open('test.json.txt', 'w') as outfile:
     json.dump(table, outfile)
table = {}
with open('test.json.txt', 'r') as infile:
    table = json.load(infile)
print table'''

