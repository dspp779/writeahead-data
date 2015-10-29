import re
rulesR = '''X prep. sth to do sth
X verb to do sth
X sth to do sth
X sth prep. doing sth
X be to do sth
X prep. sth prep. sth
X sth prep. sth
X self prep. sth
X sth to do sth
X prep. doing sth
X to do sth
X adv. prep. sth
X prep. prep. sth
X verb prep. sth
X verb sth
X prep. sth
X sth adj.
X sth adv.
X sth sth
X sth wh.
X sth that
adj. and adj.
X sth
X that
X wh.
X verb
X adv.
X adj.
X conj.'''.split('\n')

rulesL = '''adv. X
verb X
be prep. X
do mod. X
mod. X
sth do X
do prep. X
verb prep. your X
verb sth prep. X
do sth prep. X'''.split('\n')

rep = {
'X':'<H-(V|N|ADJ|ADV)P>',
'prep.':'<H-PP>',
'sth':'<I-NP>*<H-NP>',
'adv.':'<H-ADVP>',
'that':'<H-SBAR>',
'wh.':'<H-ADVP>',
'self':'<H-VP>',
'do':'<H-VP>',
'doing':'<H-VP>',
'verb':'<H-VP>',
'be':'<(I|H)-VP>',
'to':'<I-VP>',
'your':'<I-NP>',
'adj.':'<H-ADJP>',
'mod.':'<I-NP>',
'conj.':'<H-SBAR>',
'and':'<I-ADJP>',
}

regRulesR = []
for rule in rulesR:
	regRule = ''.join([rep[r] for r in rule.split()])
	regRulesR.append((regRule,rule))
	#print regRule

regRulesL = []
for rule in rulesL:
	regRule = ''.join([rep[r] for r in rule.split()])
	regRulesL.append((regRule,rule))
