import re
import numpy as np
from game import Game

def parseGameFromFile(filename):

	pattern = re.compile("NFG . . \"[^\"]*\" {[^}]*} {([^}]*)}\s*([-0-9].*$)")


	with open(filename, 'r') as in_file:
		file_content = in_file.read()
		

	match_object = re.match(pattern, file_content)
	if match_object == None:
		return "File format not valid, please use gambit-compatible .game files. (For game generation with GAMUT use the '-output GambitOutput' option)."

	dimensions = [int(x) for x in match_object.group(1).split()]

	no_players = len(dimensions)

	dimensions = [no_players]+(dimensions)

	payoff_list = [float(x) for x in match_object.group(2).split()]

	payoff_matrix = np.reshape(payoff_list, dimensions, order="F")

	payoff_matrices = []

	for i in range(no_players):
		payoff_matrices.append(payoff_matrix[i])
	
	game = Game(payoff_matrices)

	return game
