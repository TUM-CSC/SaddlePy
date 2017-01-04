''' 

'''
import numpy as np


# TODO convert ZeroSumGame in Bimatrix game, n-matrix game?

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


class ZeroSumGame(object):
	'''
	basic class for zero-sum/single matrix games
	'''

	matrix = None
	no_players = -1
	dimension = -1

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
	no_players = -1
	#TODO dimension?  (i.e. subgame is 2x1)
	indices = None
	matrix = None		# payoff matrix of the game
	submatrix = None	

	def __init__(self, matrix, indices):
		self.no_players = len(indices)
		self.indices = indices
		self.matrix = matrix
		self.computeSubgame()

	def __str__(self):
		return str(self.submatrix)

	''' function that computes the subgame payoff matrix for given game and indices 
	'''
	def computeSubgame(self):
		self.submatrix = self.matrix
		print "Compute subgame..."
		for i in range(len(self.indices)):
			#print str(i) + ", " + str(self.indices[i])
			self.submatrix = self.submatrix.take(self.indices[i], axis=i)
			#print "\n New subgame: \n" + str(self.submatrix)


	''' function to add a new action and return the new, bigger subgame '''
	def addActions(self, player_id, action_id_list):
		print "Add action " + str(action_id_list) + " for player " + str(player_id)
		self.indices[player_id].extend(action_id_list)
		list_tmp = set(self.indices[player_id])
		self.indices[player_id] = sorted(list_tmp)			# ugly type cast. Is there a way to get rid of it?

		#print self.indices
		#print "Subgame " + str(self.submatrix)

		self.computeSubgame()


class StrictSaddle(object):
	'''
	basic class for strict saddles
	representation: list of column and row indices
	'''




if __name__ == '__main__':


	'''
	@param indices: lists of lists of integers [[0,1],[1]] is the sub matrix that takes the first two rows and the second column on the game
	@return Subgame - GSP for the given starting point 
	'''
	def computeGSP(game, indices):

		subgame = Subgame(game.matrix, indices)

		change_flag = True

		#print "Compute GSP for game\n " + str(game) + "\n with subgame \n" + str(subgame) + "\n from indices " + str(indices)
		#print "Game with " + str(game.no_players) + " players of dimension " + str(game.dimension) + "."

		while change_flag:
			change_flag = False

			for i in range(game.no_players):
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
		print "Calculating dominating action..."
		notDominatedActions = []

	# computing subgame with all actions for player i
		print "Indices " + str(indices)
		allIndices = list(indices)
		print "Dimension for player " + str(game.dimension[player])
		# indices for the subgame that contains the given subgame and all actions of player i
		allIndices[player] = range(game.dimension[player])
		print "All indices " + str(allIndices)
		# indices for the subgame that contains all actions _outside_ of the given subgame for player i
		feasibleIndices = list(set(range(game.dimension[player])) - set(indices[player]))
		print "Feasible indices " + str(feasibleIndices)
		print "Game Matrix " + str(game.matrix)

		comparisonSubgame = Subgame(game.matrix, allIndices)

	# selecting one row (or column etc) from the current subgame and one outside and comparing them
		for index in feasibleIndices:
			print "Feasible index: " + str(index)
			feasibleAction = comparisonSubgame.submatrix.take(index, axis=player)
			print "Feasible action: " + str(feasibleAction)

			is_dominated = False
			for gsp_index in indices[player]:
				gsp_action = comparisonSubgame.submatrix.take(gsp_index, axis=player)
				print "GSP action: " + str(gsp_action)
				# add if feasibleAction is not dominated by any gsp_action
				if np.greater(gsp_action, feasibleAction).all():
					is_dominated = True
					break
			if not is_dominated:
				notDominatedActions.append(index)

		print "Not dominated actions " + str(notDominatedActions)
		
		# TODO work in progress, as it currently doesn't work for Zero Sum Games!!
		return notDominatedActions

	
	''' function that checks what GSPs do not contain any of the other given GSPs '''
	def findMinimalGSP(gsp_list): # inclusion minimal!
		print gsp_list
		for i in gsp_list:
			for j in gsp_list:
				if i[0] < j[0] and i[1] <= j[1]:		#TODO for more than 2 players, iterate over m dimensions
					gsp_list.remove(j)
				if i[0] <= j[0] and i[1] < j[1]:
					gsp_list.remove(j)
		return gsp_list


	game = ZeroSumGame(np.matrix('0 1 0; 1 0 0.5; 0 1 0'))
	game_article_small = ZeroSumGame(np.matrix('3 3 4; 2 3 3; 1 2 3; 2 0 5'))
	game_article_large = ZeroSumGame(np.matrix('4 2 3 5; 2 4 5 3; 2 2 3 6; 1 3 1 4; 2 1 6 1'))
	#subgame_tmp = Subgame(np.matrix('3; 2'), [[0,1],[0]])
	first_gsp = computeGSP(game_article_small, [[0,1],[0]])
	#subgame = Subgame(game, [[0,1], [2]])
	# subgame.computeSubgame() 		would be nice if this would be the identity function
	#print "Subgame payoff matrix computed"
	#subgame.addAction(1,1)		# player 1 (2nd player!!) adds action 1
	#subgame.addAction(0,2)		# player 1 (2nd player!!) adds action 2

	#computeGSP(game, (0,0))	#TODO
	#computeGSP(game, (2,1))
	#computeGSP(game, (1,2))
	
	gsp_list = list()

	gsp_1 = [set([1,2]), set([2])]
	gsp_2 = [set([1,2]), set([1,2])]
	gsp_3 = [set([3]), set([1,2])]
	gsp_list_test = list([gsp_1, gsp_2, gsp_3])
	#print findMinimalGSP(gsp_list_test)

	#for i,x in np.ndenumerate(game):		
	#		gsp_list.append(computeGSP(game,i,x))
	# print repr(gsp_list)

	action1 = Action([0,1,1,2])
	action2 = Action([1,2,2,3])
	action3 = Action([0,1,1,3])
	action4 = Action([0,1,0])

	#print "1 dominates 2?  " + str(action1.sdominates(action2))
	#print "2 dominates 1?  " + str(action2.sdominates(action1))
	#print "3 dominates 1?  " + str(action3.sdominates(action1))
	#print "4 dominates 1?  " + str(action4.sdominates(action1))
	#print "2 dominates 3?  " + str(action2.sdominates(action3))
