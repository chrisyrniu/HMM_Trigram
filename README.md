# HMM_Trigram
 
This is the solution of homework 1 for Probabilistic Graphical Models at Georgia Tech. The problems are described in the pdf file.

The Viterbi algorithm follows: https://www.youtube.com/watch?v=Bu7oSlNCmdU

1. Run Baseline:

(1) python tag_rare.py gene.train > gene.train_rare

(2) python count_freqs.py gene.train_rare > gene.counts

(3) python baseline_tagger.py gene.counts gene.test > gene_test.p1.out

(4) python eval_gene_tagger.py gene.key gene_test.p1.out

2. Run Viterbi (Trigram Features):

(1) python tag_rare.py gene.train > gene.train_rare

(2) python count_freqs.py gene.train_rare > gene.counts

(3) python viterbi_tagger.py gene.counts gene.test > gene_test.p2.out

(4) python eval_gene_tagger.py gene.key gene_test.p2.out
