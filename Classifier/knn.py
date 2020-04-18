# -*- coding: utf-8 -*-
"""KNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rn85AdBtOzXtPt_ANUwsQcL_FpfyVqCu
"""

#!pip3 install scikit-learn

#! pip3 install face_recognition

import os
import face_recognition
import pickle
from sklearn import neighbors
import numpy as np
import cv2
#from Convert_data import change_names, extract_faces
import json
import argparse
#from google.colab import drive
#drive.mount('/content/drive')

def train(conv_data_save_path, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):

    X = []
    Y = []
    #conv_data_save_path = "/content/drive/My Drive/Colab Notebooks/Converted_data"
    if conv_data_save_path is not None:
      with open(os.path.join(conv_data_save_path,"embedding.txt"), 'rb') as f:
        X = pickle.load(f)
      with open(os.path.join(conv_data_save_path,"label.txt"), 'rb') as f:
        Y = pickle.load(f)

    
    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, Y)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf



def test(result_save_path,test_data_save_path,n_neighbors):
  
  if test_data_save_path is not None:
    with open(os.path.join(test_data_save_path,"test_embedding.txt"), 'rb') as f:
      X_test = pickle.load(f)
    with open(os.path.join(test_data_save_path,"test_label.txt"), 'rb') as f:
      Y_test = pickle.load(f)
  
  results = {}
  results['predictions'] = []
  for i in range(len(X_test)):
    a = X_test[i]
    b = a.reshape(1,128)
    pred = classifier.predict(b)
    print("class : ", Y_test[i], "Prediction : ", pred)
    results['predictions'].append({'Num': i, 'Class': Y_test[i], 'Pred': int(pred[0])})
  
  print(results)
  with open(os.path.join(result_save_path,'result_knn'+str(n_neighbors)+'.json'), 'w') as outfile:  
    json.dump(results, outfile)

if __name__ == "__main__":
    # STEP 1: Train the KNN classifier and save it to disk
    # Once the model is trained and saved, you can skip this step next time.
    #test_data_save_path = sys.argv[1]
    # = "/content/drive/My Drive/Colab Notebooks/test_converted_data"
    #result_save_path = sys.argv[2]

    parser = argparse.ArgumentParser()
    parser.add_argument('--test_data_save_path', type=str, required=True, help='test data save path')
    parser.add_argument('--result_save_path', type=str, help='Results saving path')
    parser.add_argument('--conv_data_save_path', type=str,  help='path to the train directory')
    parser.add_argument('--model_save_path', type=str,  help='path to save weights file')
    parser.add_argument('--n_neighbors', type=int, default= 3, help="number of neighbours for knn")
    parser.add_argument('--train', type=bool, default= True, help="true if you want to train")
    parser.add_argument('--test', type=bool, default= True, help="true if you want to test")
    args = parser.parse_args()

    test_data_save_path = args.test_data_save_path
    result_save_path = args.result_save_path
    conv_data_save_path = args.conv_data_save_path
    model_save_path = args.model_save_path
    n_neighbors = args.n_neighbors
    train = args.train
    test = args.test

    # "/content/drive/My Drive/Colab Notebooks/Results"
    if train == True :
    	print("Training KNN classifier...")
    	classifier = train(conv_data_save_path , model_save_path n_neighbors)
    	print("Training complete!")
    if test == True :
	    print("Testing Classifier..")
    	test(result_save_path,test_data_save_path,n_neighbors)
    	print("Testing completed")

