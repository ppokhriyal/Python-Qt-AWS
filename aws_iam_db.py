#Building MongoDB Database
import os
import types
import subprocess
import pymongo
from pymongo import MongoClient

#Check if Mongod service is runnig or not
service_cmd = "pidof mongod"
proc = subprocess.Popen(service_cmd,stdout=subprocess.PIPE,shell=True)
stdout = proc.communicate()

if proc.returncode == 1 :

	print("Mongod Service is not running")
	print("Starting Mongod Service ...")
	os.system('service mongod start')

	#Establish Connection to Mongodb
	mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
	#Check if the aws_collection is available or not
	mongo_db = mongo_client["aws_iam_db"]
	mongo_collist = mongo_db.list_collection_names()
	mongo_db_dblist = mongo_client.list_database_names()

	mongo_col = mongo_db["aws_iam_collection"]

	if "aws_iam_collection" in mongo_collist and "aws_iam_db" in mongo_db_dblist:
		print("Dummy Database and Collection exists")
	else:
		print("Dummy Database and Collection does'nt exists")
		print("Creating a Dummy Database,Collection and Document")

		dummy_doc = {"user_name":"dummy_name","access_key_id":"dummy_key_id","secret_access_key":"dummy_access_key","region":"dummy_region"}
		mongo_col.insert_one(dummy_doc)

else:
	print("Mongod Service is running")

	#Establish Connection to Mongodb
	mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
	#Check if the aws_collection is available or not
	mongo_db = mongo_client["aws_iam_db"]
	mongo_collist = mongo_db.list_collection_names()
	mongo_db_dblist = mongo_client.list_database_names()

	mongo_col = mongo_db["aws_iam_collection"]


	if "aws_iam_collection" in mongo_collist and "aws_iam_db" in mongo_db_dblist:
		print("Dummy Database and Collection exists")
		name = mongo_col.find({'user_name':{'$eq':'dumsmy_name'}}).count()
		print(name)
	else:
		print("Creating Dummy Database,Collection and Document") 
		dummy_doc = {"_id":1,"user_name":"dummy_name","access_key_id":"dummy_key_id","secret_access_key":"dummy_access_key","region":"dummy_region"}
		mongo_col.insert_one(dummy_doc)



	