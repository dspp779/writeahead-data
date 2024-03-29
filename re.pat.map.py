import fileinput
from operator import methodcaller
import sys
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
from operator import methodcaller
import string
    
#mapPos = {  'TO': 'to', 'VB':'do', 'VBP':'do', 'VBD':'did', 'VBZ':'does', 'VBN':'done', 'VBG':'doing', 'JJ':'adj.', 'RB':'adv.' }

import patterns

def genPat(instance):
    
    res = [ instance[0][0].split('/')[1] ]
    for i, wordTagChunk in enumerate(instance[1:]):
        wordTag, chunk = wordTagChunk
        try:
            word, lemma, tag = wordTag.split('/')
        except:
            print >> sys.stderr, wordTag
            return '***'
        if tag == 'IN' and chunk == 'H-PP': res += [ lemma ]
        elif lemma == 'to': res += [ 'to' ]
        elif tag[:2] == 'VB' and lemma == 'be':
            res += [ lemma ] 
        elif tag == 'VBG' and chunk == 'H-VP': res += [ 'doing' ]
        elif tag == 'VBZ' and chunk == 'H-VP': res += [ 'does' ]
        elif tag == 'VBN' and chunk == 'H-VP': res += [ 'done' ]
        elif tag == 'VBD' and chunk == 'H-VP': res += [ 'did' ]
        elif tag in ['VB', 'VBP'] and chunk == 'H-VP': res += [ 'do' ]
        elif tag[:2] in ['NN', 'PR', 'NP'] and chunk == 'H-NP':
            if word in 'myself ourself ourselves yourself yourselves himself herself themself me us you him her them'.split():
                 res += [ 'someone' ]
            else: res += [ 'something' ]
        elif tag[:2] in ['NN', 'PR', 'NP'] and chunk == 'H-NP': res += [ 'something' ]
    if len(res) > 1:
        return ' '.join(res)
    else: return ''

def genIOCS(instance):
    res = [ instance[0][0].split('/')[1] ]
    for i, wordTagChunk in enumerate(instance[1:]):
        wordTag, chunk = wordTagChunk
        try:
            word, lemma, tag = wordTag.split('/')
        except:
            print >> sys.stderr, wordTag
            return '***'
        if tag == 'IN' and chunk == 'H-PP': res += [ lemma ]
        elif lemma == 'to': res += [ 'to' ]
        elif tag == 'VBG' and chunk == 'H-VP': res += [ word ]

        elif tag == 'VBZ' and chunk == 'H-VP': res += [ word ]
        elif tag == 'VBN' and chunk == 'H-VP': res += [ word ]

        elif tag in ['VB', 'VBP'] and chunk == 'H-VP': res += [ word ]
        elif tag[:2] in ['NN', 'PR', 'NP'] and chunk == 'H-NP':
            if word in 'myself ourself ourselves yourself yourselves himself herself themself me us you him her them'.split():
                 res += [ 'person' ]
            else: res += [ lemma ]
    if len(res) > 1:
        return ' '.join(res)
    else: return ''

def genNgram(instance):
    #print instance
    res = [ instance[0][0].split('/')[0] ]
    for i, wordTagChunk in enumerate(instance[1:]):
        wordTag, chunk = wordTagChunk
        try:
            word, lemma, tag = wordTag.split('/')
        except:
            print >> sys.stderr, wordTag
            return ''
        res += [ word ]

    if len(res) > 1:
        return ' '.join(res)
    else: return ''
#line = '1\tI have great difficulty to understand him .\tI have great difficulty to understand him .\tPRP VBP JJ NN TO VB PRP .\tH-NP H-VP I-NP H-NP I-VP H-VP H-NP O'.split('\n')

input_lines = 'I have great difficulty in understanding him .\tI have great difficulty in understand him .\tPRP VBP JJ NN IN VBG PRP .\tH-NP H-VP I-NP H-NP H-PP H-VP H-NP O'.split('\n')

aklWords = {x:True for x in set(re.findall('[a-z_]+', (file('data.akl.all.txt').read()+file('data.teufel.all.txt').read()).lower())) }
#print >> sys.stderr, "%s words in aklWords ..."%len(aklWords)

i = 0
#for line in input_lines: # fileinput.input():
for line in fileinput.input():
    line = line.replace('/', '|'); i = i+1
    sentNum, words, lemmas, poss, chunks = [i]+line.strip().split('\t')
    #words, lemmas, poss, chunks = line.strip().split('\t')
    words, lemmas, poss, chunks = map(methodcaller('split'), (words[0].lower()+words[1:], lemmas[0].lower()+lemmas[1:], poss, chunks))
    tagged_text = ' '.join(['/'.join(x) for x in zip(words, lemmas, poss, chunks)])
    try:
        unchunked_text = tagstr2tree(tagged_text)
    except:
        continue
    chunk_parser = RegexpChunkParser(map(lambda x:ChunkRule(*x), patterns.regRulesR), chunk_label='Pat')

    for start in range(len(unchunked_text)-1):
        word, lemma, tag = unchunked_text[start:][0][0].split('/')
        #if lemma != 'difficulty':
        #    continue
        if word not in aklWords and lemma not in aklWords:
            continue
        #print >> sys.stderr, unchunked_text[start:]
        #break
        chunked_text = chunk_parser.parse(unchunked_text[start:])
        #if chunked_text[0][0][0] not in string.ascii_lowercase:
        #    continue
        if '_label' in dir(chunked_text[0]) and chunked_text[0]._label == 'Pat':
            pat, pos = genPat(chunked_text[0][0:]), chunked_text[0][0][1][2:-1]
            if pat:
                #print '{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(pat[:pat.index(' ')]+':'+pos, pat, genIOCS(chunked_text[0][0:]), genNgram(chunked_text[0][0:], start, start+len(chunked_text[0][0:])),\
                #                                           sentNum, start, start+len(chunked_text[0][0:]), )
                try:
                    history = unchunked_text[start-1][0].split('/')[0]
                    history = history+' ' if history.isalpha() else ''
                    lookahead = unchunked_text[start+len(chunked_text[0][0:])][0].split('/')[0]
                    lookahead = ' '+ lookahead if lookahead.isalpha() else ''
                    
                    ngram = '%s[%s]%s' % (history,genNgram(chunked_text[0][0:]),lookahead)
                except:
                    ngram = '[%s]' % genNgram(chunked_text[0][0:])
                print '{}\t{}\t{}\t{}'.format(pat[:pat.index(' ')]+':'+pos, pat, genIOCS(chunked_text[0][0:]), ngram)
                #                                           sentNum, start, start+len(chunked_text[0][0:]), )
                # print '{}\t{}\t{}'.format((number+'-'+word).decode('utf-8'), pat.decode('utf-8'), ' '.join(words).decode('utf-8'))
    #break
