''' 

'''
import numpy as np



# TODO obsolete??
class Action(object):
	'''
	basic class for actions in sub-games
	'''
	def __init__(self, vector, name=None):
		self.name = name
		self.payoff = vector
		self.length = len(self.payoff)

	def getPayOffs(self):
		return self.payoff

	def sdominates(self, action):
		if (len(action.payoff) != len(self.payoff)):
			return "not comparable!"
		for i in range(len(action.payoff)):
			if self.payoff[i] <= action.payoff[i]:		# works only for 2 players #TODO change to m dimensions
				return False
		return True			

	#TODO wdominates

	def vwdominates(self, action):
		if (len(action.payoff) != len(self.payoff)):
			return "not comparable!"
		for i in range(len(action.payoff)):
			if self.payoff[i] < action.payoff[i]:		# works only for 2 players #TODO change to m dimensions
				return False
		return True


class Game(object):

	def __init__(self, matrices):
		self.matrices = matrices
		self.dimension = self.matrices[0].shape
		self.no_players = len(self.matrices)


# TODO obsolete?
class ZeroSumGame(object):
	'''
	basic class for zero-sum/single matrix games
	'''

	def __init__(self, matrix, name=None):
		self.name = name
		self.matrix = matrix
		self.dimension = self.matrix.shape
		self.no_players = len(self.matrix.shape)

	def __str__(self):
		return str(self.matrix)

	def __repr__(self):
		return repr(self.matrix)
	
	def getPayOffMatrix(self):
	        return self.matrix


class Subgame(object):
	'''
	basic class for sub games
	'''

	def __init__(self, matrices, indices):
		self.no_players = len(indices)
		self.indices = indices
		self.matrices = matrices
		self.submatrices = [None]*self.no_players
		self.computeAllSubgames()

	def __str__(self):
		string = ""
		for i in self.submatrices:
			string = string + "\n" + str(i) + "\n"
		return string

	def __eq__(self, other):
		if self.matrices == other.matrices and self.indices == other.indices:
			return True
		return False


	''' function that computes the subgame payoff matrix for given game and indices
		@param i - player id
	'''
	def computeSubgame(self, player_id):
		self.submatrices[player_id] = self.matrices[player_id]
		#print "Compute subgame..."
		for i in range(len(self.indices)):
			#print str(i) + ", " + str(self.indices[i])
			self.submatrices[player_id] = self.submatrices[player_id].take(self.indices[i], axis=i)
			#print "\n New subgame: \n" + str(self.submatrix)

	def computeAllSubgames(self):
		for i in range(self.no_players):
			self.computeSubgame(i)


	''' function to add a new action and return the new, bigger subgame '''
	def addActions(self, player_id, action_id_list):
		print "Add action " + str(action_id_list) + " for player " + str(player_id)
		self.indices[player_id].extend(action_id_list)
		list_tmp = set(self.indices[player_id])
		self.indices[player_id] = sorted(list_tmp)			# ugly type cast. TODO Is there a way to get rid of it?

		#print self.indices
		#print "Subgame " + str(self.submatrix)

		self.computeAllSubgames()






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
		#print "Calculating dominating action..."
		notDominatedActions = []

	# computing subgame with all actions for player i
		#print "Indices " + str(indices)
		allIndices = list(indices)
		#print "Dimension for player " + str(game.dimension[player])

		# indices for the subgame that contains the given subgame and all actions of player i
		allIndices[player] = range(game.dimension[player])
		#print "All indices " + str(allIndices)

		# indices for the subgame that contains all actions _outside_ of the given subgame for player i
		feasibleIndices = list(set(range(game.dimension[player])) - set(indices[player]))
		#print "Feasible indices " + str(feasibleIndices)
		#print "Game Matrix " + str(game.matrix)

		comparisonSubgame = Subgame(game.matrices, allIndices)

	# selecting one row (or column etc) from the current subgame and one outside and comparing them
		for index in feasibleIndices:
			#print "Feasible index: " + str(index)
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


	game = Game([np.matrix('0 1 0; 1 0 0.5; 0 1 0'), np.negative(np.matrix('0 1 0; 1 0 0.5; 0 1 0'))])
	payoff_player_1 = np.matrix('3 3 4; 2 3 3; 1 2 3; 2 0 5')
	game_article_small = Game([payoff_player_1, np.negative(payoff_player_1)])

	payoff_player_1_large = np.matrix('4 2 3 5; 2 4 5 3; 2 2 3 6; 1 3 1 4; 2 1 6 1')
	game_article_large = Game([payoff_player_1_large, np.negative(payoff_player_1_large)])
	strict_saddles = computeStrictSaddles(game_article_small)
	print "Strict Saddles: " + "\n--------------\n".join([str(s) for s in strict_saddles])

	# subgame.computeSubgame() 		would be nice if this would be the identity function

