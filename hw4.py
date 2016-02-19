import sys,PorterStemmer
from collections import defaultdict
from math import log


def remove_chars(word):
	word.replace('.','')
	word.replace(',','')

class Node:
	def __init__(self,n):
		self.name = n
		self.edges = []
		self.relevant_words = []
		self.mark = False
	def add_edge(self,n):
		self.edges.append(n)
	def add_word(self,w):
		self.relevant_words.append(w)

def get_node(nodes,n):
	for v in nodes:
		if v.name == n:
			return v
	return None


class Edge:
	def __init__(self,n,v):
		self.node1 = n
		self.node2 = v
		self.words = []
	def add_word(self,w):
		self.words.append(w)

def get_edge(edges,n,v):
	for e in edges:
		if (e.node1 == n) & (e.node2 == v):
			return e
		elif (e.node1 == v) & (e.node2 == n):
			return e
	return None

def dfs(v,cluster):
	cluster.append(v)
	v.mark = True
	for c in v.edges:
		if c.mark:
			continue
		elif c in clusters:
			continue
		cluster = dfs(c,cluster)
	return cluster
		


"""
stop_words = ['about','all','along','also','although','among','and','any', 'anyone', 'anything',\
	'are', 'around', 'because', 'been','before', 'being', 'both', 'but', 'came', 'come', 'coming',\
	'could', 'did', 'each', 'else', 'every', 'for', 'from',\
	'get', 'getting', 'going', 'got', 'gotten', 'had',\
	'has', 'have', 'having', 'her', 'here', 'hers', 'him', 'his', 'how',\
	'however', 'into', 'its', 'like', 'may', 'most',\
	'next', 'now', 'only', 'our', 'out', 'particular', 'same', 'she',\
	'should', 'some', 'take', 'taken', 'taking', 'than','their',\
	'that', 'the', 'then', 'there', 'these', 'they', 'this', 'those',\
	'throughout', 'too', 'took', 'very', 'was', 'went',\
	'what', 'when', 'which', 'while', 'who', 'why', 'will', 'with',\
	'without', 'would', 'yes', 'yet', 'you', 'your','one','once','twice',\
	'two', 'three', 'four', 'five', 'six', 'seven', 'eight',\
	'nine', 'ten', 'eleven', 'twelve','such','later',\
	'dozen','dozens', 'thirteen', 'fourteen', 'fifteen', 'sixteen',\
	'seventeen', 'eighteen', 'nineteen','fifth',\
	'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy',\
	'eighty', 'ninety', 'hundred','thousand', 'million']
"""



corpus_name = sys.argv[1]
param = int(sys.argv[2])
raw = open(corpus_name).read()
bios = raw.split('\n\n')
num_bios = len(bios)




#Read corpus
p = PorterStemmer.PorterStemmer()
discarded_words = []
idf_helper = defaultdict(list)
stem_helper = {}
bios_dict = defaultdict(list)

#weights_helper = []

for entry in bios:
	if len(entry) > 4:
		name = ''
		bio = entry.split('\n')
		#t = 0
		for line in bio:
			if name == '':
				name = line
			else:
				sline = line.split()
				for word in sline:
					w = word.lower()
					remove_chars(w)
					if w in stop:
						continue
					elif len(w) < 3:
						continue
					elif not w.isalpha():
						continue
					else:
						stem = p.stem(w,0,len(w)-1)
						stem_helper[stem] = w
						idf_helper[stem].append(name)
						bios_dict[name].append(stem)

						#if t < 4:
						#	if w not in weights_helper:
						#		weights_helper.append(w)
						#t +=1


# Delete useless entries
discarded_words = []
weights = defaultdict(int)
for k in idf_helper:
	if len(idf_helper[k]) > num_bios/2:
		discarded_words.append(k)
	else:
		#if k in weights_helper:
		#	weights[k] = -log(len(idf_helper[k])/num_bios,2) + 3
		weights[k] = -log(len(idf_helper[k])/num_bios, 2)
for k in discarded_words:
	del idf_helper[k]


#Create undirected graph
EDGES = []
for word in idf_helper:
	for n in idf_helper[word]:
		for v in idf_helper[word]:
			if n != v:
				e = get_edge(EDGES,n,v)
				if e == None:
					e = Edge(n,v)
					EDGES.append(e)
				e.add_word(word)

#Delete edges between nodes with weight below parameter
delete = []
for e in EDGES:
	weight = 0
	for w in e.words:
		weight += weights[w]
	if weight < param:
		delete.append(e)
for e in delete:
	EDGES.remove(e)

#Connect nodes
NODES = []
for e in EDGES:
	n1 = get_node(NODES,e.node1)
	n2 = get_node(NODES,e.node2)
	if n1 == None:
		n1 = Node(e.node1)
		NODES.append(n1)
	if n2 == None:
		n2 = Node(e.node2)
		NODES.append(n2)
	n1.add_edge(n2)
	n2.add_edge(n1)
	for w in e.words:
		if w not in n1.relevant_words:
			n1.add_word(w)
		if w not in n2.relevant_words:
			n2.add_word(w)

for k in bios_dict:
	v = get_node(NODES,k)
	if v == None:
		NODES.append(Node(k))

#DFS plus clusters
clusters = []
for n in NODES:
	if n.mark:
		continue
	cluster = dfs(n,[])
	clusters.append(cluster)


#names for clusters
names = []
for i in range(0,len(clusters)):
	best = -1
	best_name = ''
	for j in range(0,len(clusters[i])):
		for w in clusters[i][j].relevant_words:
			if weights[w] > best:
				best = weights[w]
				best_name = w
	if best_name != '':
		names.append(best_name)
	else:
		n = clusters[i][0]
		best = -1
		best_word = ''
		for w in bios_dict[n.name]:
			val = weights[w]
			if val > best:
				best = val
				best_word = w
		names.append(best_word)

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

#print out the clusters
for i in range(0,len(clusters)):
	print('Cluster Title: ', stem_helper[names[i]])
	for j in range(0,len(clusters[i])):
		print(clusters[i][j].name)
	print()







