#!/usr/bin/env python3

import sys 
import math

test_file = sys.argv[1]
model_file = sys.argv[2]
sys_output = open(sys.argv[3], 'w')

model = {} #{class : {feature : weight}}
classes = []

#read in model file
with open(model_file, 'r') as model_data:

	for line in model_data:
		line = line.strip()
		tokens = line.split(' ')

		if tokens[0] == 'FEATURES':
			class_label = tokens[-1]
			classes.append(class_label)
			model[class_label] = {}
		else:
			feature = tokens[0]
			weight = float(tokens[1])
			model[class_label][feature] = weight


#for line in test_data
with open(test_file, 'r') as test_data:

	sys_output.write('%%%%% test data:\n')
	linecount = 0

	confusion_matrix = [[0 for i in range(3)] for j in range(3)]
	i = 0
	j = 0

	for line in test_data:
		line = line.strip()
		tokens = line.split(' ')

		true_label = tokens[0]

		Z = 0;
		results = {}
		probs = {}

		for c in classes:
			sum_c = model[c]['<default>']

			for t in tokens[1:]:
				pair = t.split(':')
				word = pair[0]
				if word in model[c]:
					sum_c += model[c][word]

			results[c] = math.exp(sum_c)
			Z += results[c]

		for r in results:
			probs[r] = results[r]/float(Z)

		system_out = max(probs, key=lambda key: probs[key])

		#count incorrect and correct responses
		if true_label == 'talk.politics.guns':
			tl = 0
		elif true_label == 'talk.politics.mideast':
			tl = 1
		elif true_label == 'talk.politics.misc':
			tl = 2

		if system_out == 'talk.politics.guns':
			so = 0
		elif system_out == 'talk.politics.mideast':
			so = 1
		elif system_out == 'talk.politics.misc':
			so = 2

		confusion_matrix[tl][so] = confusion_matrix[tl][so] + 1

		#sort probabilities dictionary by value to print in order
		sorted_probs = sorted(probs.items(), key=lambda item: item[1], reverse=True)

		#print to sys_output file
		output = ''
		for item in sorted_probs:
			label = item[0]
			prob = item[1]
			output += ' ' + label + ' ' + "{0:.5f}".format(prob)

		sys_output.write('array:' + str(linecount) + ' ' + true_label + str(output) + '\n')
		linecount += 1

	#calculate accuracy from confusion matrix values
	total = confusion_matrix[0][0] + confusion_matrix[0][1] + confusion_matrix[0][2] + confusion_matrix[1][0] + confusion_matrix[1][1] + confusion_matrix[1][2] + confusion_matrix[2][0] + confusion_matrix[2][1] + confusion_matrix[2][2]
	correct = confusion_matrix[0][0] + confusion_matrix[1][1] + confusion_matrix[2][2] 
	accuracy = correct/total

	print('Confusion matrix for the test data:')
	print('row is the truth, column is the system output')
	print()
	print('             talk.politics.guns talk.politics.mideast talk.politics.misc')
	print('talk.politics.guns ' + str(confusion_matrix[0][0]) + ' ' + str(confusion_matrix[0][1]) + ' ' + str(confusion_matrix[0][2]))
	print('talk.politics.mideast ' + str(confusion_matrix[1][0]) + ' '  + str(confusion_matrix[1][1]) + ' '  + str(confusion_matrix[1][2]))
	print('talk.politics.misc ' + str(confusion_matrix[2][0]) + ' '  + str(confusion_matrix[2][1]) + ' '  + str(confusion_matrix[2][2]))
	print()
	print(' Test accuracy=' + "{0:.5f}".format(accuracy))
	print()
	print()

sys_output.close()







