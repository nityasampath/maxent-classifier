#!/usr/bin/env python3

import sys 
import math

training_file = sys.argv[1]
output_file = sys.argv[2]

if len(sys.argv) > 3:
	model_file = sys.argv[3]
	model = {} #{class : {feature : weight}}

training_data = {} #{instance : feat list}
inst_num = 0 #N
classes = [] #set of class labels, to calculate P(y | x)
model_exps = {} #{class : {feat : model exp}}


#read in model file if given
if len(sys.argv) > 3:

	with open(model_file, 'r') as model_data:

		for line in model_data:
			line = line.strip()
			tokens = line.split(' ')

			if tokens[0] == 'FEATURES':
				class_label = tokens[-1]
				model[class_label] = {}
			else:
				feature = tokens[0]
				weight = float(tokens[1])
				model[class_label][feature] = weight

#read in training data
with open(training_file, 'r') as data:

	for line in data:
		line = line.strip()
		tokens = line.split(' ')

		class_label = tokens[0]

		if class_label not in classes:
			classes.append(class_label)

		feat_list = tokens[2:]

		inst_num += 1

		inst_label = 'inst' + str(inst_num)

		training_data[inst_label] = feat_list

class_num = len(classes)

P = 1.0/class_num #P(y|x) if no model file given

for label in classes:
	model_exps[label] = {}

#iterate through training insts
for inst, features in training_data.items(): #for each inst x in training data

	#calculate P(y|x) if model file given
	if len(sys.argv) > 3:
		Z = 0;
		results = {}
		probs = {}

		for c in classes:
			sum_c = model[c]['<default>']

			for t in features:
				pair = t.split(':')
				word = pair[0]
				if word in model[c]:
					sum_c += model[c][word]

			results[c] = math.exp(sum_c)
			Z += results[c]

		for r in results:
			probs[r] = results[r]/float(Z)


	for f in features:
	 	pair = f.split(':')
	 	t = pair[0]
	 	for y in classes:
	 		if len(sys.argv) > 3:
	 			P = probs[y]
	 			if t not in model_exps[y]:
		 			model_exps[y][t] = 1.0/inst_num * P
			 	else:
			 		model_exps[y][t] += 1.0/inst_num * P
	 		else:
		 		if t not in model_exps[y]:
		 			model_exps[y][t] = 1.0/inst_num * P
			 	else:
			 		model_exps[y][t] += 1.0/inst_num * P


#print empirical expectations
output = open(output_file, 'w')

for class_label in classes:

	for feat in sorted(model_exps[class_label].keys()):
		model_exp = model_exps[class_label][feat]
		output.write(class_label + ' ' + feat + ' ' + "{0:.5f}".format(model_exp) + ' ' + "{0:.5f}".format(model_exp * inst_num) + '\n')





