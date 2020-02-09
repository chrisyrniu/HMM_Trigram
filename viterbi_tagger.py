import sys
from collections import defaultdict

def generate_list(corpus_file):

	wordtag_list = []
	gram1_list = []
	gram2_list = []
	gram3_list = []

	l = corpus_file.readline()
	while l:
		line = l.strip()
		if line:
			fields = line.split(" ")
			if fields[1] == "WORDTAG":
				counts_wordtag = int(fields[0])
				ne_tag = fields[2]
				word = " ".join(fields[3:])
				wordtag_list.append((counts_wordtag, ne_tag, word))

			if fields[1] == "1-GRAM":
				counts_gram1 = int(fields[0])
				ne_tag = fields[2]
				gram1_list.append((counts_gram1, ne_tag)) 

			if fields[1] == "2-GRAM":
				counts_gram2 = int(fields[0])
				ne_tag1 = fields[2]
				ne_tag2 = fields[3]
				gram2_list.append((counts_gram2, ne_tag1, ne_tag2))

			if fields[1] == "3-GRAM":
				counts_gram3 = int(fields[0])
				ne_tag1 = fields[2]
				ne_tag2 = fields[3]
				ne_tag3 = fields[4]
				gram3_list.append((counts_gram3, ne_tag1, ne_tag2, ne_tag3))	

		l = corpus_file.readline()
	return wordtag_list, gram1_list, gram2_list, gram3_list

def count_emission(wordtag_list, gram1_list):
	emission = defaultdict(int)
	tag_list = []
	for i in gram1_list:
		tag_list.append(i[1])

	for j in wordtag_list:
		emission[(j[1], j[2])] = j[0] / gram1_list[tag_list.index(j[1])][0]

	return emission

def comp_con_prob(gram2_list, gram3_list):
	con_prob = {}
	for i in gram3_list:
		for j in gram2_list:
			if i[1] == j[1] and i[2] == j[2]:
				con_prob[(i[1], i[2], i[3])] = i[0] / j[0] 
	return con_prob

def generate_test(test_file):
	temp = []
	test_list = []
	l = test_file.readline()
	while l:
		line = l.strip()
		if line:
			fields = line.split(" ")
			word = " ".join(fields[:])
			temp.append(word) 
		else:
			test_list.append(temp)
			temp = []
		l = test_file.readline()	

	return test_list

def viterbi(sentence_init, emission, con_prob):
	tags = []
	pi = {}
	bp = {}
	pi[(0, "*", "*")] = 1

	sentence = []

	for word in sentence_init:	
		n = 0
		for a in emission.keys(): 
			if a[1] == word:
				sentence.append(word)
				n = 1
				break
		if n == 0:
			sentence.append("_RARE_")

	for k in range(1, len(sentence) + 1):
		if k == 1:
			su = ["*"]
			sv = ["O", "I-GENE"]
			sw = ["*"]
		if k == 2:
			su = ["O", "I-GENE"]
			sv = ["O", "I-GENE"]
			sw = ["*"]
		if k > 2:
			su = ["O", "I-GENE"]
			sv = ["O", "I-GENE"]
			sw = ["O", "I-GENE"]	

		for u in su:
			for v in sv:
				temp = []
				temp_w = []
				for w in sw:
					# if emission[(v, sentence[k-1])] == 0:
					# 	emission[(v, sentence[k-1])] = 0.00001
					temp.append(pi[(k-1, w, u)] * con_prob[(w, u, v)] * emission[(v, sentence[k-1])])
					temp_w.append(w)
				pi[(k, u, v)] = max(temp)
				bp[(k, u, v)] = temp_w[temp.index(max(temp))]

	temp1 = []
	temp_u = []
	temp_vv = []
	for u in ["O", "I-GENE"]:
		temp2 = []
		temp_v = []
		for v in ["O", "I-GENE"]:
			temp2.append(pi[len(sentence), u, v] * con_prob[(u, v, "STOP")])
			temp_v.append(v)
		temp1.append(max(temp2))
		temp_u.append(u)
		temp_vv.append(temp_v[temp2.index(max(temp2))])

	tags.append(temp_vv[temp1.index(max(temp1))])
	tags.append(temp_u[temp1.index(max(temp1))])

	for k in range(len(sentence) - 2, 0, -1):
		yk = bp[(k+2, tags[-1], tags[-2])]
		tags.append(yk)

	tags.reverse()

	return tags

def tagger(test_list, emission, con_prob):
	tag_list = []
	for i in test_list:
		temp = viterbi(i, emission, con_prob)
		tag_list.append(temp)
	return tag_list

def write(test_list, tag_list, output):
	for i in range(len(test_list)):
		for j in range(len(test_list[i])):
			output.write("%s %s\n" %(test_list[i][j], tag_list[i][j]))
		output.write("\n")

if __name__ == "__main__":

	if len(sys.argv)!=3:
		usage()
		sys.exit(2)

	input1 = open(sys.argv[1], "r")
	input2 = open(sys.argv[2], "r")
	
	wordtag_list, gram1_list, gram2_list, gram3_list = generate_list(input1)
	emission = count_emission(wordtag_list, gram1_list)
	con_prob = comp_con_prob(gram2_list, gram3_list)
	test_list = generate_test(input2)
	tag_list = tagger(test_list, emission, con_prob)
	write(test_list, tag_list, sys.stdout)

