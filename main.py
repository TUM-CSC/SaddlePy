''' 

'''
import sys
import numpy as np
from game import Game, Subgame
from parser import parseGameFromFile
from printer import printSaddlesToFile, printSaddleSizeToFile






if __name__ == '__main__':


	'''
	function that computes the smallest GSP that includes a given sub matrix
	@param indices: lists of lists of integers [[0,1],[1]] is the sub matrix that takes the first two rows and the second column on the game
	@return Subgame - GSP for the given starting point 
	'''
	def computeGSP(game, indices):

		subgame = Subgame(game.matrices, indices)

		change_flag = True

		while change_flag:
			change_flag = False

			for i in range(game.no_players):
				#print "Subgame prior to finding dominated actions: \n" + str(subgame)
				notDominatedActions = findNotDominatedActions(game, indices, subgame, i)		# needs to add each action consecutively
				if notDominatedActions:
					change_flag = True
				subgame.addActions(i, notDominatedActions)

		return subgame


	'''
	function that finds actions that are not strictly dominated by a actions due to chosen subgame in one dimension
	@param game Game
	@param player int - player ID
	@return [int] 
	'''
	def findNotDominatedActions(game, indices, subgame, player):
		#print "Calculating dominating actions..."
		notDominatedActions = []

	# computing subgame with all actions for player i
		allIndices = list(indices)

		# indices for the subgame that contains the given subgame and all actions of player i
		allIndices[player] = range(game.dimension[player])

		# indices for the subgame that contains all actions _outside_ of the given subgame for player i
		feasibleIndices = list(set(range(game.dimension[player])) - set(indices[player]))

		comparisonSubgame = Subgame(game.matrices, allIndices)

	# selecting one row (or column etc) from the current subgame and one outside and comparing them
		for index in feasibleIndices:
			feasibleAction = comparisonSubgame.submatrices[player].take(index, axis=player)
			#print "Feasible action: " + str(feasibleAction)

			is_dominated = False
			for gsp_index in allIndices[player]:
				action = comparisonSubgame.submatrices[player].take(gsp_index, axis=player)
				# add if feasibleAction is not dominated by any gsp_action
				if np.greater(action, feasibleAction).all():
					is_dominated = True
					break
			if not is_dominated:
				notDominatedActions.append(index)

		#print "Not dominated actions " + str(notDominatedActions)
		
		return notDominatedActions



	
	''' function that finds inclusion minimal GSPs from a given list of GSPs
		@param gsp_list [Subgame] - list of subgames
	'''
	def findMinimalGSP(gsp_list):
		minimal_gsp_list = list(gsp_list)				# necessary as iteration through the list is faulty due to removal of elements otherwise
		for i in gsp_list:
			for j in gsp_list:
				gsp_matrix_i = i.indices
				gsp_matrix_j = j.indices
				# check subset property via comparing the indices (!! only yields correct result for GSPs of the same game !!)
				if i <= j and i != j:
					# if GSP j is a superset of GSP i, it gets removed from the minimal GSP set
					if j in minimal_gsp_list:
						#print "GSP " + str(j) + " was removed."
						minimal_gsp_list.remove(j)
		return minimal_gsp_list


	def computeStrictSaddles(game):
		gsp_list = []
		for i,x in np.ndenumerate(game.matrices[0]):
			#print str(i) + ", " + str(x)
			indices = [[j] for j in i]
			#print "indices: " + str(indices)
			gsp_tmp = computeGSP(game, indices)
			#print "Matrix element " + str(x) + " GSP " + str(gsp_tmp)
			if not gsp_tmp in gsp_list:
				gsp_list.append(gsp_tmp)

		gsp_list = findMinimalGSP(gsp_list)
		return gsp_list



	filename_in = sys.argv[1]
	filename_out = sys.argv[2]

	game = parseGameFromFile(filename_in)
	strict_saddles = computeStrictSaddles(game)


	# size of the strict saddles. Currently looks only at first player; modify for non-symmetric games
	size_list = []
	for i in strict_saddles:
		size_list.append(i.getSize()[0])


	#print "Print saddle size to file"
	out_counter = filename_out + "/counters/" + (str(game.dimension[0]) + ".txt")
	printSaddleSizeToFile(out_counter, size_list[0])


	#print "Print saddle to file"
	filename_out = filename_in.split('.')[0] + ".saddle"
	printSaddlesToFile(filename_out, strict_saddles)


	# two litlle build in examples
	game = Game([np.matrix('0 1 0; 1 0 0.5; 0 1 0'), np.negative(np.matrix('0 1 0; 1 0 0.5; 0 1 0'))])
	game_article_small = Game([np.matrix('3 3 4; 2 3 3; 1 2 3; 2 0 5'), np.negative(np.matrix('3 3 4; 2 3 3; 1 2 3; 2 0 5'))])

	#print "Strict Saddles: " + "\n--------------\n".join([str(s) for s in strict_saddles])



