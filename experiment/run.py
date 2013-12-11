#!/usr/bin/env python

import xml.dom.minidom
import os

#---------------------------------------------------------#
# main function definition
def main() :
  #print input_algoid, input_dataid
  try :
    root = xml.dom.minidom.parse("exp.conf")
  except:
    print "[error] load config file failed!" 
    return -1

  algo = extract_algo(root)
  data = extract_data(root)
  input_algo_id = choose_algo(algo)
  if input_algo_id < 0 or input_algo_id >= len(algo) : 
     print "\ninput number is invalid. \nquit"
     return -1
  input_data_id = choose_algo(data)
  if input_data_id < 0 or input_data_id >= len(data) :
     print "\ninput number is invalid. \nquit"
     return -1

  ret = run_exp(algo, data, input_algo_id, input_data_id)
  return ret

#----------------------------------------------------------#
# extract_algo: extract the algorithm setting
def extract_algo(config) :
  algoid_max = -1 
  algo = []

  for algo_sec in config.getElementsByTagName("algorithm")[0].childNodes:
    algo_info = {}
    if algo_sec.nodeType == algo_sec.ELEMENT_NODE :
      algoid = int(algo_sec.getAttribute("id"))
      if algoid_max < algoid:
        algoid_max = algoid

      # extract the algo name
      extract = algo_sec.getElementsByTagName("name")
      if len(extract) > 0 :
        algo_info["name"] = extract[0].childNodes[0].data.encode("ascii").strip()
      
      # extract the train path
      extract = algo_sec.getElementsByTagName("train")
      if len(extract) > 0 :
        algo_info["train"] = extract[0].childNodes[0].data.encode("ascii").strip()
     
      # extract the train para
      extract = algo_sec.getElementsByTagName("train_para")
      if len(extract) > 0 :
        algo_info["train_para"] = extract[0].childNodes[0].data.encode("ascii").strip()
     
      # extract the model file
      extract = algo_sec.getElementsByTagName("model")
      if len(extract) > 0 :
        algo_info["model"] = extract[0].childNodes[0].data.encode("ascii").strip()

      # extract the model file
      extract = algo_sec.getElementsByTagName("predict")
      if len(extract) > 0 :
        algo_info["predict"] = extract[0].childNodes[0].data.encode("ascii").strip()

      # extract the model file
      extract = algo_sec.getElementsByTagName("result")
      if len(extract) > 0 :
        algo_info["result"] = extract[0].childNodes[0].data.encode("ascii").strip()

      # extract the model file
      extract = algo_sec.getElementsByTagName("cv")
      if len(extract) > 0 :
        algo_info["cv"] = extract[0].childNodes[0].data.encode("ascii").strip()

      # extract the model file
      extract = algo_sec.getElementsByTagName("cv_para")
      if len(extract) > 0 :
        algo_info["cv_para"] = extract[0].childNodes[0].data.encode("ascii").strip()

      algo.append(algo_info)

  return algo

#----------------------------------------------------------#
def extract_data(config) :
  dataid_max = -1 
  data = []

  for data_sec in config.getElementsByTagName("data")[0].childNodes:
    data_info = {}
    if data_sec.nodeType == data_sec.ELEMENT_NODE :
      dataid = int(data_sec.getAttribute("id"))
      if dataid_max < dataid:
        dataid_max = dataid

      # extract the data name
      extract = data_sec.getElementsByTagName("name")
      if len(extract) > 0 :
        data_info["name"] = extract[0].childNodes[0].data.encode("ascii").strip()
      
      # extract the train data path
      extract = data_sec.getElementsByTagName("train")
      if len(extract) > 0 :
        data_info["train"] = extract[0].childNodes[0].data.encode("ascii").strip()

     # extract the algo name
      extract = data_sec.getElementsByTagName("test")
      if len(extract) > 0 :
        data_info["test"] = extract[0].childNodes[0].data.encode("ascii").strip()
     
      data.append(data_info)

  return data

#----------------------------------------------------------------------------#
# print all algorithm names and choose one of them
def choose_algo(algo) :
  try :
    print "---------------------------------------------"
    print "There are %d algorithms:" %(len(algo))
    for index in range(0, len(algo)) :
      print index,": ", algo[index]["name"]
    input_algo = input("You choose: ")
  except :
    return -1

  return input_algo

#----------------------------------------------------------------------------#
# print all data set names and choose one of them
def choose_data(data) :
  try :
    print "---------------------------------------------"
    print "There are %d data:" %(len(data))
    for index in range(0, len(data)) :
      print index,": ", data[index]["name"]
    input_data = input("You choose: ")
  except :
    return -1

  return input_data

#----------------------------------------------------------------------------#
# run the exp according to the selected algo and data
def run_exp(algo, data, input_algo_id, input_data_id) :
  try:
    cmd_train = algo[input_algo_id]["train"] + " " + \
                algo[input_algo_id]["train_para"] + " " + \
                data[input_data_id]["train"] + " " + \
                algo[input_algo_id]["model"]
    print "Training starts......"
    print cmd_train
    os.system(cmd_train)
    cmd_predict_train = algo[input_algo_id]["predict"] + " " + \
                        data[input_data_id]["train"] + " " + \
                        algo[input_algo_id]["model"] + " " + \
                        algo[input_algo_id]["result"]
    cmd_predict_test = algo[input_algo_id]["predict"] + " " + \
                       data[input_data_id]["test"] + " " + \
                       algo[input_algo_id]["model"] + " " + \
                       algo[input_algo_id]["result"]
    print "Testing starts......"
    print "Predict on Training:"
    print cmd_predict_train
    os.system(cmd_predict_train)
    print "Predict on Testing:"
    print cmd_predict_test
    os.system(cmd_predict_test)
    if algo[input_algo_id].has_key("cv"):
      cmd_crossvalidate = algo[input_algo_id]["cv"] + " " + \
                          algo[input_algo_id]["cv_para"] + " " + \
  		          data[input_data_id]["train"]
      print "Cross validation starts......"
      print cmd_crossvalidate
      os.system(cmd_crossvalidate)

  except:
    print "parameter setting has errors"
    return -1

  return 1;

#----------------------------------------------------------------------------#
if __name__ == '__main__' :
  main()

