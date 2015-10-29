

zcat citeseerx.gz | ./lmapreduce.sh 64m 80 "python re.pat.map.coll.py" "cat" map.out
cat map.out/* | ./lmapreduce.sh 64m 80 "cat" "python re.pat.reduce.py" reduce.out

Note: for 10G dataset, #MapJobs = 10000/64 = 156 #ReduceJobs = 80

Output directory: map.out
Elasped time: 5:16:59
Output directory: reduce.out
Elasped time: 0:05:26

zcat citeseerx.gz | ./lmapreduce.sh 64m 80 "python re.pat.map.coll.py" "cat" re.map.out
cat re.map.out/* | ./lmapreduce.sh 64m 80 "cat" "python re.pat.reduce.py" re.reduce.out

Note: for 10G dataset, #MapJobs = 10000/64 = 156 #ReduceJobs = 80

Output directory: re.map.out
Elasped time: 5:42:31
Output directory: re.reduce.out
Elasped time: 0:05:43

Test case:

We introduce a method for learning query transformations that improves the ability to retrieve answers to questions from an information retrieval system. During the training stage the method involves automatically learning phrase features for classifying questions into different types, automatically generating candidate query transformations from a training set of question/answer pairs, and automatically evaluating the candidate transforms on target information retrieval systems such as real-world general purpose search engines. At run time, questions are transformed into a set of queries, and re-ranking is performed on the documents retrieved. We present a prototype search engine, Tritus, that applies the method to web search engines. Blind evaluation on a set of real queries from a web search engine log shows that the method significantly outperforms the underlying web search engines as well as a commercial search engine specializing in question answering.



{"bat:N": [178, ["bat in something", 49, [["of [bats in flight]", 1, 2]]], ["bat do something", 25, [["whether individual [bats have signature chirps]", 1, 2]]], ["bat be", 25, [["that many [bats are] social", 13, 1]]], ["bat do", 17, [["where [bats hibernate]", 2, 2]]], ["bat of something", 14, [["to nectarivorous [bats of the Glossophaginae]", 5, 1]]], ["bat from something", 13, [["that [bats from Laguna] and", 1, 1]]], ["bat to something", 13, [["with a baseball [bat to the head]", 1, 1]]]],
	
WSD and 翻譯 

bat in something
	of [bats in flight] 在飛行中的蝙蝠

bat do something
	whether individual [bats have signature chirps] 無論是個人蝙蝠有特色啁啾

bat be
	that many [bats are] social 許多蝙蝠是群居

bat do
	where [bats hibernate] 蝙蝠冬眠

bat of something
	to nectarivorous [bats of the Glossophaginae] 長舌葉鼻蝠屬的食蜜蝙蝠

bat from something
	that [bats from Laguna] and 從麗蝙蝠

bat to something
	with a baseball [bat to the head] 用棒球棒頭部
