import sys
from collections import defaultdict

def generate_list(corpus_file):

	wordtag_list = []
	gram1_list = []

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

		l = corpus_file.readline()
	return wordtag_list, gram1_list


def compute_emission(wordtag_list, gram1_list):
	emission = defaultdict(int)
	tag_list = []
	for i in gram1_list:
		tag_list.append(i[1])

	for j in wordtag_list:
		emission[(j[1], j[2])] = j[0] / gram1_list[tag_list.index(j[1])][0]

	return emission

def estimator(test_file, emission):
	test_list = []
	l = test_file.readline()
	while l:
		line = l.strip()
		if line:
			fields = line.split(" ")
			word = " ".join(fields[:])
			test_list.append(word) 
		else:
			test_list.append(None)
		l = test_file.readline()	

	estimate_list = []
	for i in test_list:
		if i:
			emission_tag = []
			emission_prob = []
			for a, b in emission.items():
				if a[1] == i:
					emission_tag.append(a[0])
					emission_prob.append(b)
			if emission_prob:
				estimate_list.append(emission_tag[emission_prob.index(max(emission_prob))])
			else:
				for a, b in emission.items():
					if a[1] == "_RARE_":
						emission_tag.append(a[0])
						emission_prob.append(b)
				estimate_list.append(emission_tag[emission_prob.index(max(emission_prob))])
		else:
			estimate_list.append(None)

	return test_list, estimate_list

def write(test_list, estimate_list, output):
	for i in range(len(test_list)):
		if test_list[i]:
			output.write("%s %s\n" %(test_list[i], estimate_list[i]))
		else:
			output.write("\n")

if __name__ == "__main__":

	if len(sys.argv)!=3:
		usage()
		sys.exit(2)

	input1 = open(sys.argv[1], "r")
	input2 = open(sys.argv[2], "r")
	
	wordtag_list, gram1_list = generate_list(input1)
	emission = compute_emission(wordtag_list, gram1_list)
	test_list, estimate_list = estimator(input2, emission)
	write(test_list, estimate_list, sys.stdout)

