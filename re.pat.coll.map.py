import sys, fileinput
from operator import methodcaller

from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *

import patterns

# awl3000: Academic Word List 
# format: HEADWORD<tab>', '.join([other words])<tab>definition
def awl_line_to_words(line):
    headword, wordlist_str, definition = line.strip().split('\t')
    wordlist = wordlist_str.split(', ')
    return [ headword ] + wordlist
awl3000 = [ word for words in map(awl_line_to_words, open('data.awl.all.txt')) for word in words ]

# longman3000: most common 3000 words in longman dictioinary
# format: phrase<tab>'/'.join([possible tags])<tab>in most common n thousand in spoken/written English (Sn/Wn)
def longman3k_line_to_word(line):
    tokens = line.strip().split()
    word = ' '.join(tokens[:-2])
    tags = tuple(tokens[-2].split('/'))
    # spoken common level/written common level
    level = tuple(tokens[-1].split('/', 1))
    return word, tags, level
longman3000 = [ word for word, tags, _ in map(longman3k_line_to_word, open('data.longman.3000.txt')) if any(tag in {'n','v','adj','adv'} for tag in tags) ]

# pdev: Pattern Dictionary of English Verbs
# format: word<tab>num_of_pattern<tab>Status<tab>BNC50<tab>BNC<tab>OEC
# status: complete: complete, WIP: work-in-progress, NYS: not yet started
pdev = map(lambda x: x.strip().split('\t', 1)[0], open('data.pdev.verbs.all.txt'))

aklWords = set(awl3000+longman3000+pdev)

personPronouns = 'i you he she me him her us my our your their his her them someone somebody anyone anybody'.split() # we
determiners = 'a an the this that these those a an any another other what'.split()
prepositions = ('above about across against along among around at before behind below beneath between beyond '
                'by down during except for from in inside into like near of off on since to toward towards through '
                'under until up upon with within').split()
conjunctions = 'and or but yet so nor'.split()
functionWords = set(personPronouns+determiners+prepositions+conjunctions)

# pronouns
subject_personal_pronouns = set('i you he she we they'.split())
object_personal_pronouns = set('me you him her us them'.split())
intensive_personal_pronouns = set('myself yourself himself herself ourself ourselves yourselves themselves'.split())


# TODO: pattern generation refinement
# 1. The iteration should iterate over chunks instead of words,
# because some nouns are in multiple words. ex. 9 PM, the teacher,...
# 2. more precise label 'something': label classification
# someone, time, place, 
def genPat(instance):
    res = [ instance[0][0].split('/')[1] ]
    for i, wordTagChunk in enumerate(instance[1:]):
        wordTag, chunk = wordTagChunk
        try:
            word, lemma, tag = wordTag.split('/')
        except:
            print >> sys.stderr, wordTag
            return '***'
        if tag == 'IN' and chunk == 'H-PP':
            res += [ lemma ]
        elif lemma == 'to':
            res += [ 'to' ]
        elif tag[:2] == 'VB' and lemma == 'be':
            res += [ 'be' ] 
        elif tag == 'VBG' and chunk == 'H-VP':
            res += [ 'doing' ]
        elif tag == 'VBZ' and chunk == 'H-VP':
            res += [ 'does' ]
        elif tag == 'VBN' and chunk == 'H-VP':
            res += [ 'done' ]
        elif tag == 'VBD' and chunk == 'H-VP':
            res += [ 'did' ]
        elif tag in ['VB', 'VBP'] and chunk == 'H-VP':
            res += [ 'do' ]
        elif tag[:2] in ['NN', 'PR', 'NP'] and chunk == 'H-NP':
            if word in intensive_personal_pronouns:
                res += [ 'oneself' ]
            if word in object_personal_pronouns:
                res += [ 'someone' ]
            else:
                res += [ 'something' ]
        elif tag[:2] in ['NN', 'PR', 'NP'] and chunk == 'H-NP': res += [ 'something' ]
    if len(res) > 1:
        return ' '.join(res)
    return ''

def genIOCS(instance):
    res = [ instance[0][0].split('/')[1] ]
    for i, wordTagChunk in enumerate(instance[1:]):
        wordTag, chunk = wordTagChunk
        try:
            word, lemma, tag = wordTag.split('/')
        except:
            print >> sys.stderr, wordTag
            return '***'
        if tag == 'IN' and chunk == 'H-PP':
            res += [ lemma ]
        elif lemma == 'to': res += [ 'to' ]
        elif tag == 'VBG' and chunk == 'H-VP':
            res += [ word ]
        elif tag == 'VBZ' and chunk == 'H-VP':
            res += [ word ]
        elif tag == 'VBN' and chunk == 'H-VP':
            res += [ word ]
        elif tag in ['VB', 'VBP'] and chunk == 'H-VP':
            res += [ word ]
        elif tag[:2] in ['NN', 'PR', 'NP'] and chunk == 'H-NP':
            if word in object_personal_pronouns or word in intensive_personal_pronouns:
                res += [ 'person' ]
            else:
                res += [ lemma ]
    if len(res) > 1:
        return ' '.join(res)
    return ''

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
    return ''
#line = '1\tI have great difficulty to understand him .\tI have great difficulty to understand him .\tPRP VBP JJ NN TO VB PRP .\tH-NP H-VP I-NP H-NP I-VP H-VP H-NP O'.split('\n')

input_lines = 'I have great difficulty in understanding him .\tI have great difficulty in understand him .\tPRP VBP JJ NN IN VBG PRP .\tH-NP H-VP I-NP H-NP H-PP H-VP H-NP O'.split('\n')
input_lines = 'I have great paper in understanding him .\tI have great paper in understand him .\tPRP VBP JJ NN IN VBG PRP .\tH-NP H-VP I-NP H-NP H-PP H-VP H-NP O'.split('\n')

if __name__ == '__main__':
    # for line in input_lines:
    for sent_no, line in enumerate(fileinput.input()):
        line = line.strip().replace('/', '|')
        words, lemmas, poss, chunks = line.split('\t')
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
            # filter out function words or words not in aklWords
            if (word not in aklWords and lemma not in aklWords) or lemma in functionWords:
                continue
            chunked_text = chunk_parser.parse(unchunked_text[start:])
            if hasattr(chunked_text[0], '_label') and chunked_text[0]._label == 'Pat':
                pat, pos = genPat(chunked_text[0]), chunked_text[0][0][1][2:-1]
                if pat:
                    #print '{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(pat[:pat.index(' ')]+':'+pos, pat, genIOCS(chunked_text[0][0:]), genNgram(chunked_text[0][0:], start, start+len(chunked_text[0][0:])),\
                    #                                           sent_no, start, start+len(chunked_text[0][0:]), )
                    try:
                        # fetch history from the beginning of the sentence
                        history = ' '.join(map(lambda x:x.split('/', 1)[0], unchunked_text[:start][0]))
                        # Or fetch one chunk ahead
                        # prev = [ index for index in range(start) if chunks[index][0] == 'H']
                        # if prev:
                        #     history = ' '.join(words[max(prev):start])+' '
                        # else:
                        #     history = ''
                        lookahead = unchunked_text[start+len(chunked_text[0])][0].split('/')[0]
                        lookahead = ' '+ lookahead if lookahead.isalpha() else ''
                        
                        ngram = '%s[%s]%s' % (history, genNgram(chunked_text[0][0:]), lookahead)
                    except:
                        ngram = '[%s]' % genNgram(chunked_text[0])
                    print '{}\t{}\t{}\t{}'.format(pat[:pat.index(' ')]+':'+pos, pat, genIOCS(chunked_text[0][0:]), ngram)
                    #                                           sent_no, start, start+len(chunked_text[0][0:]), )
                    # print '{}\t{}\t{}'.format((number+'-'+word).decode('utf-8'), pat.decode('utf-8'), ' '.join(words).decode('utf-8'))
        #break
