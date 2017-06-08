def printSaddlesToFile(filename, saddles):

	saddle_string = ""

	for i in saddles:
		saddle_string = saddle_string + "SS: "
		index_string = ""
		for indices in i.indices:
			index_string = index_string + "["
			for j in range(len(indices)):
				if j == len(indices)-1:
					index_string = index_string + str(indices[j]) + "] "	
				else:
					index_string = index_string + str(indices[j]) + ","
		saddle_string = saddle_string + index_string + "\n"


	with open(filename, 'w') as out_file:

		out_file.write(saddle_string)
		#print "Writing\n" + saddle_string + "to file \'" + filename + "\'"
		print saddle_string


# TODO write non-overwriting!
def printSaddleSizeToFile(filename, saddlesize):

	with open(filename, 'w') as out_file:
		size_string = str(saddlesize) + " "	
		out_file.write(size_string)




