#!/usr/bin/env python
from KnowledgeBase import KnowledgeBase
from Classifiers import ML_Controller, KnowledgeIntegrator
import NEMO
import MySQLdb
from collections import deque
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import threading, sys, os, time, json, traceback, pandas, numpy
import copy

class NELController:
    def __init__(self, facts_file, config_file):
        with open(facts_file) as fd:
            json_data = json.load(fd)

        self.NEMO = NEMO.NEMO(config_file)

        classifiers = json_data['Classifiers']
        for classifier in classifiers:
            created_classifier = self.createClassifier(classifier)


    def createClassifier(self, class_dict):
        #print (class_dict)
        classifier_name = class_dict['Classifier_Name']
        data_source = class_dict['Data_Source']
        algorithm = class_dict['Algorithm']
        target = class_dict['Target']
        features = class_dict['Features']
        #features = self.parseFeatures(features)
        kb = self.NEMO.getDataSourceFromName(data_source) #will need copy constructor for KnowledgeBase
        all_feats = kb.X
        all_feats.append(kb.Y)
        x,y = self.parseFeatures(features, target, all_feats)

    def parseFeatures(self, feature_string, target, all):
        print(feature_string)
        if feature_string[0] == '{':
            print("Case 1")
            feature_string = feature_string.strip('{}')
            print (feature_string)
            features = features_string.split(',')
            print (features)
            return(features,target)
        elif len(feature_string) >= 4 and feature_string[4] == '-':
            print("Case 2")

        elif feature_string == 'ALL':
            print("Case 3")
        else:
            print("Invalid feature string")

        #case1: {}
            #make list of strings
        #case2: ALL - {}
            #get all column names and remove
        #case3: ALL
            #get all but target

def main():
    facts = "config/facts.json"
    NELController(facts, "config/config.json")

if __name__ == '__main__':
    main()
