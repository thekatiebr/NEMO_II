from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix, accuracy_score, precision_score, f1_score, recall_score
import pandas
from pandas import DataFrame
import pandas.io.sql as psql
import KnowledgeBase
import random

class DecisionTreeController:

	def __init__(self, kb):
		#print "This will be a decision tree"
		self.algorithm_name = "Decision Tree"
		self.algorithm_id = ""
		random.seed()
		for i in range(1,10):
			self.algorithm_id = self.algorithm_id + str(random.randint(1,9))
		
		self.kb = kb
		
	def createModel(self, x, y, attributes=None):
		self.x = x
		self.y = y 
		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(x,y)
		
		if attributes is not None:
			self.tree = DecisionTreeClassifier(random_state=None)
			self.set_params(attributes)
		else:
			self.tree = DecisionTreeClassifier(random_state=0)
			
		self.tree.fit(self.X_train, self.y_train)

	def createModelFromID(self, x, y, id):
		#run query
		stmt = "select * from ModelRepository where algorithm_id = " + id
		self.kb.executeQuery(stmt)
		row = self.kb.fetchOne()
		attributes = {}
		while row != None:
			#print row
			key = row[2]
			val = row[3]
			#print key + ": " + val
			if val == 'None' or val == 'NULL':
				val = None
			if val is not None:
				if key in ['max_features', 'max_depth', 'max_leaf_nodes', 'random_state']:
					val = int(val)
				elif key in ['min_weight_fraction_leaf', 'min_impurity_split']:
					val = float(val)
				elif key in ['min_samples_split', 'min_samples_leaf']:
					lst = list(val)
					if lst.count('.') > 0:
						val = float(val)
					else:
						val = int(val)	
			#print type(val)
 			attributes[key] = val
			row = self.kb.fetchOne()
		self.createModel(x,y,attributes)
		
	def copyModel(self,x,y,id):
		self.algorithm_id = id
		self.createModelFromID(x,y,id)
		
	def runModel(self, multi=False):
		predictions = self.tree.predict(self.X_test)	
		av = ''
		if not multi:
			av = 'binary'
		else:
			av = 'micro'
		accuracy = accuracy_score(self.y_test,predictions)
		precision = precision_score(self.y_test,predictions, average=av)
		recall = recall_score(self.y_test, predictions, average=av)
		f1 = f1_score(self.y_test,predictions, average=av)
		cm = confusion_matrix(self.y_test,predictions)
		
		self.results = {'ID': self.algorithm_id, 'Name': self.algorithm_name, 'Accuracy': accuracy, 'Precision': precision, 'Recall': recall, 'F1': f1, 'Confusion_Matrix': cm}
		
		to_return =  (self.algorithm_id, self.algorithm_name, accuracy, precision, recall, f1, cm)
		self.kb.removeCurrentModel(self)
		return to_return

		
	def set_params(self, attr):
		self.tree.set_params(**attr)
		
	def get_params(self):
		return self.tree.get_params()
		
	def optimize(self, metric, method):
		if method == 'Coordinate Ascent':
			return self.coordinateAscent(metric)

	def coordinateAscent(self, metric):
		best_model = self
		#test other criterion
		#print "in coordinate ascent"
		best_model = self.optimizeCriterion(metric, self)
		#test other max_features
			
		return best_model
	
	def optimizeMaxFeatures(self, metric, best_model):
		best_model_attributes = best_model.get_params()
		#sqrt
		sqrt_tree = DecisionTreeController(self.kb)
		sqrt_attr = best_model_attributes
		sqrt_attr['max_features'] = 'sqrt'
		sqrt_tree.createModel(self.x, self.y, sqrt_attr)
		sqrt_tree.runModel(self.kb.multi)
		
		#log2
		log_tree = DecisionTreeController(self.kb)
		log_attr = best_model_attributes
		log_attr['max_features'] = 'log2'
		log_tree.createModel(self.x, self.y, log_attr)
		log_tree.runModel(self.kb.multi)
		
		#test between sqrt and log2
		if(sqrt_tree.results.get(metric) >= best_model.results.get(metric) and sqrt_tree.results.get(metric) >= log_tree.results.get(metric)):
			return sqrt_tree
		if(log_tree.results.get(metric) >= best_model.results.get(metric) and log_tree.results.get(metric) >= sqrt_tree.results.get(metric)):
			return log_tree
		else:
			return best_model
		#random percent
		best_metric = 0
		best_percent_model = None
		for i in range(1,100):
			curr = i/100.0
			percent_attr = best_model_attributes.get_params()
			percent_attr['max_features'] = curr
			percent_tree = DecisionTreeController(self.kb)
			percent_tree.createModel(self.x, self.y, percent_attr)
			percent_tree.runModel(self.kb.multi)
			if percent_tree.results.get(metric) >= best_metric:
				best_percent_model = percent_tree
		
		if best_percent_model.results.get(metric) >= best_model.results.get(metric):
			return best_percent_model
		else:
			return best_model
			
	def optimizeCriterion(self, metric, best_model):
		attributes = best_model.get_params()
		attributes['criterion'] = "entropy" if attributes['criterion'] == 'gini' else 'gini'
		
		criterion_tree = DecisionTreeController(self.kb)
		criterion_tree.createModel(self.x, self.y, attributes)
		criterion_tree.runModel(self.kb.multi)
		if(criterion_tree.results.get(metric) >= best_model.results.get(metric)):
			return criterion_tree		
		else:
			return best_model