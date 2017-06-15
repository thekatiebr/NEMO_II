from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import KnowledgeBase

##############################################################################################################
# ML-Controller class																					     #
# SKLearn interface for NEMO																		 		 #
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
class ML_Controller:
	#Constructor
	#imports data from knowledge base
	#Preconditions:
	# * A knowledge base has been set up and read data
	#Postconditions: 
	# * Data will be imported from the 
	def __init__(kb):
		