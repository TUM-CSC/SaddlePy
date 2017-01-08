import re

def parseGameFromFile(filename):

	pattern = re.compile("NFG . . \"[^\"]*\" {[^}]*} {([^}]*)}\s*([-0-9].*$)")



	with open(filename, 'r') as in_file:
		file_content = in_file.read()
		match_object = re.match(pattern, file_content)
		if match_object == None:
			return "File format not valid, please use gambit-compatible .game files. (For game generation with GAMUT use the '-output GambitOutput'."
		print match_object.group(1)
		print match_object.group(2)

	dimensions = [int(x) for x in match_object.group(1).split()]
	payoff_list = [float(x) for x in match_object.group(2).split()]

	print "Payofflist: " + str(payoff_list)
	print "Dimensions: " + str(dimensions)
		

	#with open(filename, 'r') as in_file:
	#	for line in in_file:
	#		print line
	return filename
