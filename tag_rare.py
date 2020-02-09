import sys
from collections import defaultdict

def corpus_iterator(corpus_file):

	corpus_list = []
	l = corpus_file.readline()
	while l:
		line = l.strip()
		if line:
			fields = line.split(" ")
			ne_tag = fields[-1]
			word = " ".join(fields[:-1])
			corpus_list.append((word, ne_tag)) 
		else:
			corpus_list.append((None, None))
		l = corpus_file.readline()
	return corpus_list

def count(corpus_iterator):

	counter = defaultdict(int)
	for l in corpus_iterator:
		if l[0]:
			counter[l[0]] += 1
	return counter

def write(iterator, counter, output):
	for l in iterator:
		if l[0]:
			if counter[l[0]] >= 5:
				output.write("%s %s\n" %(l[0], l[1]))
			else:
				output.write("_RARE_ %s\n" %l[1])
		else:
			output.write("\n")


if __name__ == "__main__":

    if len(sys.argv)!=2: 
        usage()
        sys.exit(2)

    try:
        input = open(sys.argv[1],"r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)	


    iterator = corpus_iterator(input)
    counter = count(iterator)
  
    write(iterator, counter, sys.stdout)