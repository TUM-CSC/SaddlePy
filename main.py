''' 

'''
import sys
import numpy as np
from game import Game, Subgame
from parser import parseGameFromFile






if __name__ == '__main__':


	'''
	@param indices: lists of lists of integers [[0,1],[1]] is the sub matrix that takes the first two rows and the second column on the game
	@return Subgame - GSP for the given starting point 
	'''
	def computeGSP(game, indices):

		subgame = Subgame(game.matrices, indices)

		change_flag = True

		#print "Compute GSP for game\n " + str(game) + "\n with subgame \n" + str(subgame) + "\n from indices " + str(indices)
		#print "Game with " + str(game.no_players) + " players of dimension " + str(game.dimension) + "."

		while change_flag:
			change_flag = False

			for i in range(game.no_players):
				print "Subgame prior to finding dominated actions: \n" + str(subgame)
				notDominatedActions = findNotDominatedActions(game, indices, subgame, i)		# needs to add each action consecutively
				if notDominatedActions:
					change_flag = True
				subgame.addActions(i, notDominatedActions)

		return subgame


	'''
	function that finds actions that are not strictly dominated by a actions due to chosen subgame in one dimension
	@param game ZeroSumGame (later on probably any game?)
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
			print "Feasible action: " + str(feasibleAction)

			is_dominated = False
			for gsp_index in allIndices[player]:
				action = comparisonSubgame.submatrices[player].take(gsp_index, axis=player)
				# add if feasibleAction is not dominated by any gsp_action
				if np.greater(action, feasibleAction).all():
					is_dominated = True
					break
			if not is_dominated:
				notDominatedActions.append(index)

		print "Not dominated actions " + str(notDominatedActions)
		
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
				if i.indices < j.indices and i.indices <= j.indices:
					# if GSP j is a superset of GSP i, it gets removed from the minimal GSP set
					if j in minimal_gsp_list:
						#print "GSP " + str(j) + " was removed."
						minimal_gsp_list.remove(j)
		return minimal_gsp_list


	def computeStrictSaddles(game):
		gsp_list = []
		for i,x in np.ndenumerate(game.matrices[0]):
			print str(i) + ", " + str(x)
			indices = [[j] for j in i]
			print "indices: " + str(indices)
			gsp_tmp = computeGSP(game, indices)
			print "Matrix element " + str(x) + " GSP " + str(gsp_tmp)
			if not gsp_tmp in gsp_list:
				gsp_list.append(gsp_tmp)

		gsp_list = findMinimalGSP(gsp_list)
		return gsp_list

	print "Sys Arguments " + str(sys.argv)
	filename = sys.argv[1]

	print parseGameFromFile(filename)

	


	game = Game([np.matrix('0 1 0; 1 0 0.5; 0 1 0'), np.negative(np.matrix('0 1 0; 1 0 0.5; 0 1 0'))])
	payoff_player_1 = np.matrix('3 3 4; 2 3 3; 1 2 3; 2 0 5')
	game_article_small = Game([payoff_player_1, np.negative(payoff_player_1)])

	payoff_player_1_large = np.matrix('4 2 3 5; 2 4 5 3; 2 2 3 6; 1 3 1 4; 2 1 6 1')
	game_article_large = Game([payoff_player_1_large, np.negative(payoff_player_1_large)])
	#strict_saddles = computeStrictSaddles(game_article_print)
	#small "Strict Saddles: " + "\n--------------\n".join([str(s) for s in strict_saddles])

	# subgame.computeSubgame() 		would be nice if this would be the identity function

