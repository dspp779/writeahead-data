import fileinput
from operator import methodcaller
import sys
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
from operator import methodcaller
import string

awl3000 = [ (x, 'awl') for x in list(set(re.findall('[a-z_]+', file('data.awl.all.txt').read()))) ]
#print awl3000, len(awl3000), 'paper' in awl3000

longman3000 = [ x.strip().split(' ')[:2] for x in file('data.longman.3000.txt').readlines() if x.strip().split(' ')[1] in ['n','v','adj','adv'] ]
#print longman3000
#print 'paper' in longman3000
    
pdev = [ x.strip().split('\t')[:3] for x in file('data.pdev.verbs.all.txt').readlines() ]
pdev = dict([ (x[0], x[-1]) for x in pdev]+longman3000+awl3000)
aklWords = { x:True for x in set(pdev.keys()+re.findall('[a-z_]+', (file('data.akl.all.txt').read()+file('data.teufel.all.txt').read()).lower())) \
                    if (x not in pdev) or (pdev[x] in ['WIP', 'complete', 'NYS', 'n','v','adj','adv', 'awl'])}

personPronouns = 'i you he she me him her us my our your their his her them someone somebody anyone anybody'.split() # we
determiners = 'a an the this that these those a an any another other what'.split()
prepositions = 'above about across against along among around at before behind below beneath between beyond by down during except for from in inside into like near of off on since to toward towards through under until up upon with within'.split()
conjunctions = 'and or but yet so nor'.split()

functionWords = dict([ (x, True) for x in personPronouns+determiners+prepositions+conjunctions ])

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
input_lines = 'I have great paper in understanding him .\tI have great paper in understand him .\tPRP VBP JJ NN IN VBG PRP .\tH-NP H-VP I-NP H-NP H-PP H-VP H-NP O'.split('\n')

i = 0
for line in input_lines: # fileinput.input(): # input_lines: # fileinput.input(): # input_lines: # fileinput.input(): 
    line = line.replace('/', '|'); i = i+1
    sentNum, words, lemmas, poss, chunks = [i]+line.strip().split('\t')
    #words, lemmas, poss, chunks = line.strip().split('\t')
    words, lemmas, poss, chunks = map(methodcaller('split'), (words[0].lower()+words[1:], lemmas[0].lower()+lemmas[1:], poss, chunks))
    tagged_text = ' '.join(['/'.join(x) for x in zip(words, lemmas, poss, chunks)])
    try:
        unchunked_text = tagstr2tree(tagged_text.encode('utf8'))
    except:
        continue
    chunk_parser = RegexpChunkParser(map(lambda x:ChunkRule(*x), patterns.regRulesR), chunk_label='Pat')

    for start in range(len(unchunked_text)-1):
        word, lemma, tag = unchunked_text[start:][0][0].split('/')
        #if lemma != 'difficulty':
        #    continue
        if (word not in aklWords and lemma not in aklWords) or lemma in functionWords:
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
                    prev = [ index for index in range(start) if chunks[index][0] == 'H']
                    if prev:
                        history = ' '.join(words[max(prev):start])+' '
                    else:
                        history = ''
                    lookahead = unchunked_text[start+len(chunked_text[0][0:])][0].split('/')[0]
                    lookahead = ' '+ lookahead if lookahead.isalpha() else ''
                    
                    ngram = '%s[%s]%s' % (history,genNgram(chunked_text[0][0:]),lookahead)
                except:
                    ngram = '[%s]' % genNgram(chunked_text[0][0:])
                print '{}\t{}\t{}\t{}'.format(pat[:pat.index(' ')]+':'+pos, pat, genIOCS(chunked_text[0][0:]), ngram)
                #                                           sentNum, start, start+len(chunked_text[0][0:]), )
                # print '{}\t{}\t{}'.format((number+'-'+word).decode('utf-8'), pat.decode('utf-8'), ' '.join(words).decode('utf-8'))
    #break
