''' 

'''
import numpy as np

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
		self.submatrix = self.computeSubgame()

	def __str__(self):
		return str(self.submatrix)

	''' function that computes the subgame payoff matrix for given game and indices '''
	def computeSubgame(self):
		self.submatrix = self.matrix
		print "Compute subgame..."
		for i in range(len(self.indices)):
			print str(i) + ", " + str(self.indices[i])
			self.submatrix = self.submatrix.take(self.indices[i], axis=i)
			print "New subgame: " + str(self.submatrix)
		return self.submatrix

	''' function to add a new action and return the new, bigger subgame '''
	def addAction(self, player_id, action_id):
		print "Add action " + str(action_id) + " for player " + str(player_id)
		print self.indices
		print self.indices[player_id]
		self.indices[player_id].append(action_id)
		self.indices[player_id].sort()

		print self.indices
		print "Subgame " + str(self.submatrix)

		self.submatrix = self.computeSubgame()


class StrictSaddle(object):
	'''
	basic class for strict saddles
	representation: list of column and row indices
	'''




if __name__ == '__main__':


	'''
	@param indices: lists of lists of integers [[0,1],[1]] is the sub matrix that takes the first two rows and the second column on the game
	'''
	def computeGSP(game, indices):

		subgame = Subgame(game.matrix, indices) 

		print "Compute GSP for game\n " + str(game) + "\n with subgame \n" + str(subgame) + "\n from indices " + str(indices)
		print "Game with " + str(game.no_players) + " players of dimension " + str(game.dimension) + "."

		for i in range(game.no_players):
			dominatingActions = findDominatingAction(game, indices, subgame)
			print subgame.indices
			print "Indices: " + str(subgame.indices[i]) 
			#subgame.indices[i].add(dominatingActions)
			
			print i
		#TODO
		gsp = subgame
		return gsp

	def findDominatingAction(game, indices, subgame):
		print "Calculating dominating action..."
		#TODO
		return None
	
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
