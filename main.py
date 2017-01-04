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

	def __init__(self, matrix, name=None):
	        self.name = name
	        self.matrix = matrix
	
	def getPayOffMatrix(self):
	        return self.matrix

class Subgame(object):
	'''
	basic class for sub games
	'''
	no_players = -1
	#TODO dimension?  (i.e. subgame is 2x1)
	indices = None
	game = None
	subgame = None		#necessary??

	def __init__(self, game, indices):
		self.no_players = len(indices)
		self.indices = indices
		self.game = game
		self.subgame = self.computeSubgame()

	''' function that computes the subgame payoff matrix for given game and indices '''
	def computeSubgame(self):
		self.subgame = self.game
		print "Compute subgame..."
		for i in range(len(self.indices)):
			print str(i) + ", " + str(self.indices[i])
			self.subgame = self.subgame.take(self.indices[i], axis=i)
			print "New subgame: " + str(self.subgame)
		return self.subgame

	''' function to add a new action and return the new, bigger subgame '''
	def addAction(self, player_id, action_id):
		print "Add action " + str(action_id) + " for player " + str(player_id)
		print self.indices
		print self.indices[player_id]
		self.indices[player_id].append(action_id)
		self.indices[player_id].sort()

		print self.indices
		print "Subgame " + str(self.subgame)

		self.subgame = self.computeSubgame()		# updates the subgame payoff matrix. Maybe better/faster to just add the columns/rows


class StrictSaddle(object):
	'''
	basic class for strict saddles
	representation: list of column and row indices
	'''




if __name__ == '__main__':


	def computeGSP(matrix, index, element=None):
		element = matrix[index]
		# print str(position)
		#TODO
		return [set([1,2]), set([2])]
	
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


	game = np.matrix('0 1 0; 1 0 0.5; 0 1 0')
	subgame = Subgame(game, [[0,1], [2]])
	print "Subgame initialized"
	# subgame.computeSubgame() 		would be nice if this would be the identity function
	print "Subgame payoff matrix computed"
	subgame.addAction(1,1)		# player 1 (2nd player!!) adds action 1
	#subgame.addAction(0,2)		# player 1 (2nd player!!) adds action 2

	#computeGSP(game, (0,0))	#TODO
	#computeGSP(game, (2,1))
	#computeGSP(game, (1,2))
	
	gsp_list = list()

	gsp_1 = [set([1,2]), set([2])]
	gsp_2 = [set([1,2]), set([1,2])]
	gsp_3 = [set([3]), set([1,2])]
	gsp_list_test = list([gsp_1, gsp_2, gsp_3])
	print findMinimalGSP(gsp_list_test)

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
