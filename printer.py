def printSaddlesToFile(filename, saddles, saddle_type):

	saddle_string = ""

	for i in saddles:
		if (saddle_type == "s"):
			saddle_string = saddle_string + "SS: "

		# TODO weak saddles

		if (saddle_type == "v"):
			saddle_string = saddle_string + "VS: "

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

def printStrictSaddlesToFile(filename, saddles):

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

# TODO streamline with strict saddles!!
def printVeryWeakSaddlesToFile(filename, saddles):

	saddle_string = ""

	for i in saddles:
		saddle_string = saddle_string + "VWS: "
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


def printSaddleSizeToFile(filename, saddlesize):
	
	with open(filename, 'a') as out_file:
		size_string = str(saddlesize) + " "	
		out_file.write(size_string)



