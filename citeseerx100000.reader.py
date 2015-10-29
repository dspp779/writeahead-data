#!/usr/bin/env python 
# -*- coding: utf-8 -*-
    
if __name__ == '__main__':
    fileout = file('citeseerx100000.tag.txt', 'w')
    for line in file('citeseerx100000.txt').readlines():
        word, lemma, pos, chunk = [ x.split() for x in line.split('\t') ]
        print >> fileout, ' '.join( [ '/'.join(x) for x in zip(lemma, pos) ] )
    fileout.close()
    