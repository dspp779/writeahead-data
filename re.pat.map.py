#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import sys, os, fileinput
from itertools import imap, islice, product

# patterns
reservedWords = { 'to', 'so', 'not', 'where', 'which',
                  'that', 'as', 'if', 'though', 'and',
                  'by', 'with', 'together', 'way', 'into' }
Vpatterns = set('V, V n, V pl-n, V pron-refl, V-amount, V -ing, '
                'V to-inf, V inf, V that, V wh, V wh to-inf, '
                'V quote, V so, V not, V as if, V as though, '
                'V and v, '
                'V prep, V adv, V together, V prep n, V as adj, '
                'V as to wh, V by amount, V by -ing, '
                'V n n, V n adj, V n -ing, V n to-inf, V n inf, '
                'V n that, V n wh, V n wh to-inf, V n quote, V n -ed, '
                'V n prep, V n adv, V n with adv, V pl-n with together, '
                'V way prep, V way adv, V n prep n, V n as adj, '
                'V n as to wh, V n into -ing'.split(', '))
Npatterns = set("N that, N to-inf, the N, N -ing, N 's ADJST, "
                "N about inf, N prep n, N of amount N of pl-n, "
                "N of n as n, N of n to n, N of n with n, "
                "N on n for n, N on n to-inf, N ord ADJ?, "
                "N to n that, N to n to-inf, N with n for n, "
                "N with n that, N with n to-inf, N for n to-inf, "
                "N from n for n, N from n that N from n to-inf, "
                "N from n to n,"
                "number N, n of N, n to N, "
                "on N, with N, within N, without N, in N, "
                "N be, there be N, there BE ? about N".split(', '))
Apatterns = set('a ADJ amount, ADJ adj, ADJ and adj, ADJ that, ADJ to-inf, ADJ enough, ADJ -ing, ADJ n, ADJ wh however ADJ, '
                'ADJ prep n, ADJ after -ing, ADJ as to wh, ADJ enough n, ADJ enough PREP2 n, ADJ in color, ADJ onto -ing n, '
                'ADJ PREP1 n for? n, ADJ to n for -ing n, ADJ enough for n to-inf, ADJ enough that, ADJ enough to-inf, '
                'ADJ enough n for n, ADJ enough n for n to-inf, ADJ enough n that, ADJ enough n to-inf, ADJ n for n, '
                'ADJR n than clause, ADJR n than n, ADJR n than prep, ADJR than done n, ADJR than adj, ADJR than someway, '
                'adv. ADJ, adv. ADJ n, amount ADJ, as ADJ as COMP, how ADJ COMP2, however ADJ'.split(', '))
allTemplate = Vpatterns | Npatterns | Apatterns

# pronouns
subject_personal_pronouns = set('i you he she we they'.split())
object_personal_pronouns = set('me you him her us them'.split())
intensive_personal_pronouns = set('myself yourself himself herself ourself ourselves yourselves themselves'.split())


def genElement(word, lemma, tag, phrase):
    res = []
    # if lemma in reservedWords: res += [lemma, ]
    # if phrase[0] == 'H' and tag == 'VB': res += ['V', 'v', 'inf']
    # if phrase[0] == 'H' and tag == 'VB': res += ['V', 'v', 'inf']
    
    if lemma in reservedWords: res += [ lemma ]
    if tag in {'WDT', 'WP', 'WP$', 'WRB'}: res += ['wh']
    if phrase[0] == 'H':
        if phrase == 'H-PP': res += [ 'prep' ]
        if tag == 'CD': res += [ 'amount' ]
        if tag == 'IN': res += [ lemma ]
        elif tag in {'JJ', 'JJR', 'JJS'}: res += [ 'ADJ', 'adj' ]
        elif tag == {'RB', 'RBR', 'RBS', 'RP'}: res += [ 'ADV', 'adv' ]
        elif tag in {'NN', 'NNS', 'NNP', 'NNPS'}: res += [ 'N', 'n' ]
        elif tag[:2] == 'VB' and lemma == 'be': res += [ 'be' ]
        elif tag == 'VB': res += [ 'V', 'v', 'inf' ]
        elif tag == 'VBD': res += [ 'V', 'v', '-ed' ]
        elif tag == 'VBN': res += [ 'V', '-ed' ]
        elif tag == 'VBG': res += [ 'V', '-ing' ]
        elif tag == 'VBP': res += [ 'V', 'v', 'inf' ]
        elif tag == 'VBZ': res += [ 'V', 'v' ]
        elif tag == 'PRP': res += [ 'n' ]
    elif phrase[0] == 'I' and not res:
        res += [ '' ]
    elif phrase == 'O':
        return []
    return res

def genPattern(template, words, lemmas):
    res = []
    headword = ''
    for tag, word, lemma in zip(template, words, lemmas):
        if tag:
            if tag.isupper():
                headword = (headword if headword else lemma, tag)
                res += [ lemma ]
            elif tag in {'prep', 'wh'}: res += [ lemma ]
            else: res += [ tag ]

            # if word in intensive_personal_pronouns: res = [ 'oneself' ]
            # if word in object_personal_pronouns: res = [ 'someone' ]
            # else: res = [ 'something' ]
    return headword, ' '.join(res)

def to_str(elements):
    return ' '.join(filter(lambda x: x[0] if x else x, elements))

def findGoodPat(words, lemmas, tags, phrases):
    def next_n_chunk_distance(phrases, n):
        count = 0
        for i, phrase in enumerate(phrases):
            if phrase[0] == 'H':
                count += 1
                if count > n:
                    return i
            elif phrase[0] == 'O':
                return i
        return len(phrases)
                
    # generate elements such as V, N, ADV...
    elements = [ genElement(*x) for x in zip(words, lemmas, tags, phrases) ]
    length = len(elements)
    for i in range(length-1):
        # start from concrete elements (not empty or blank)
        if not(elements[i] and elements[i][0]): continue
        for j in range(i+2, min(i+10, length+1))[::-1]:
            # elements[i:j] contains no empty element and does not end with blank element
            if [] in elements[i:j] or not elements[j-1][0]: continue
            # in template
            templates = [ template for template in product(*elements[i:j]) if to_str(template) in allTemplate ]
            for template in templates:
                headword, pat = genPattern(template, words[i:j], lemmas[i:j])
                headword = '%s:%s' % headword
                col = ' '.join(lemmas[i:j])
                history = ' '.join(words[:i]) + ' ' if i > 0 else ''
                lookahead_index = j + next_n_chunk_distance(phrases[j:], 1)
                lookahead = ' ' + ' '.join(words[j:lookahead_index]) if lookahead_index > j else ''
                sent = '%s[%s]%s' % (history, ' '.join(words[i:j]), lookahead)
                yield headword, pat, col, sent
            if templates:
                break

if __name__ == '__main__':
    for i, line in enumerate(fileinput.input()):
        # if i != 167: continue
        if not line: continue
        line = line.decode('utf-8').strip()
        # print i, line
        words, lemmas, tags, phrases = [ x.split(' ') for x in line.split('\t') ]

        for patInfo in findGoodPat(words, lemmas, tags, phrases):
            # out = headword.encode('unicode_escape') + '\t' + pat.encode('unicode_escape')
            # if len(out.strip()) == 0:
            #     exit()
            # print patInfo
            print '\t'.join( info.encode('unicode_escape') for info in patInfo )
        # prinst
        # print
        # if res:
        #     print res