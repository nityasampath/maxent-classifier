#!/usr/bin/env python3

import sys 

training_file = sys.argv[1]

training_data = {} #{class : {instance : feat list}}
inst_num = 0 #N
classes = []
emp_exps = {} #{class : {feat : emp exp}}
raw_counts = {} #{class : {feat : num insts}}

#read in training data
with open(training_file, 'r') as data:

	for line in data:
		line = line.strip()
		tokens = line.split(' ')

		class_label = tokens[0]
		if class_label not in training_data:
			training_data[class_label] = {}

		if class_label not in classes:
			classes.append(class_label)

		feat_list = tokens[2:]

		inst_num += 1

		inst_label = 'inst' + str(inst_num)

		training_data[class_label][inst_label] = feat_list

for label in classes:
	emp_exps[label] = {}
	raw_counts[label] = {}

#iterate through training insts
for class_label, insts in training_data.items():

	for inst, features in insts.items():

		for f in features:
			pair = f.split(':')
			t = pair[0]
			for y in classes:
				if y == class_label:
					if t not in emp_exps[y]:
						emp_exps[y][t] = 1.0/inst_num
					else:
				 		emp_exps[y][t] += 1.0/inst_num

					if t not in raw_counts[y]:
				 		raw_counts[y][t] = 1
					else:
						raw_counts[y][t] += 1
				else:
					if t not in emp_exps[y]:
				 		emp_exps[y][t] = 0.0
					if t not in raw_counts[y]:
				 		raw_counts[y][t] = 0


#print empirical expectations
for class_label in classes:

	for feat in sorted(emp_exps[class_label].keys()):
		emp_exp = emp_exps[class_label][feat]
		print(class_label + ' ' + feat + ' ' + "{0:.5f}".format(emp_exp) + ' ' + str(raw_counts[class_label][feat]))













