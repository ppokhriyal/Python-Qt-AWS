import sys
import os
import time
import getpass
import boto3
import pymongo
import subprocess
from botocore.exceptions import ClientError, EndpointConnectionError
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSlot
from mainwindow import Ui_MainWindow

class aws_iam_mainwindow(QtWidgets.QMainWindow):

	def __init__(self):
		super(aws_iam_mainwindow,self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		#Set Focus to Access Key ID
		self.ui.access_key_id_lineEdit.setFocus(True)
		#Call aws-iam-db.py,in order to create the Database and Collection
		os.system("python3 /var/opt/PyQt-AWS-IAM/aws_iam_db.py")

		#Building Mongodb Connection
		mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
		mongo_db = mongo_client["aws_iam_db"]
		mongo_col = mongo_db["aws_iam_collection"]

		#Check out the user name who invoked this script
		self.ui.access_user.setText(getpass.getuser())

		#Check if the user have document ready
		if mongo_col.find({'user_name':{'$eq':'getpass.getuser()'}}).count() != 1:
			print("user document not available")
			self.statusBar().showMessage("No Database Found",3000)
		else:
			print("Database available")	

		#Submit button Clicked
		self.ui.submit_btn.clicked.connect(self.submit_btn)
		#Clear button Clicked
		self.ui.clear_btn.clicked.connect(self.clear_btn)
		

	def submit_btn(self):

		print("SUBMIT BUTTON CLICKED")

		#Check if Access Key Id, Secrect Access Key and Region field is not empty
		if len(self.ui.access_key_id_lineEdit.text()) == 0 or len(self.ui.secret_access_key_lineEdit.text()) == 0 or len(self.ui.region_lineEdit.text()) == 0:
			QMessageBox.critical(self, "Error"," Please Fill all the fields\n\n Access Key Id, Secrect Access Key and Region")

		else:

			self.ui.submit_btn.setDisabled(True)
			self.ui.clear_btn.setDisabled(True)

			#Now check if the user is root or not
			if getpass.getuser() == 'root':
				print("Creating AWS Environment for root user")

				#Remove and Create the .aws directory
				os.system('rm -rf /root/.aws')
				os.makedirs("/root/.aws")

				#Creating AWS Credential file
				file_credential = open("/root/.aws/credentials","w")
				file_credential.writelines("[default]\naws_access_key_id = {}\naws_secret_access_key = {}\n".format(self.ui.access_key_id_lineEdit.text(),self.ui.secret_access_key_lineEdit.text()))
				file_credential.close()

				#Create AWS Config file
				file_config = open("/root/.aws/config","w")
				file_config.writelines("[default]\nregion={}\n".format(self.ui.region_lineEdit.text()))
				file_config.close()

				#Check the AWS Credentials
				

				aws_cred_cmd = "python3 /var/opt/PyQt-AWS-IAM/test_aws_credentials.py"
				proc = subprocess.Popen(aws_cred_cmd,stdout=subprocess.PIPE,shell=True)
				stdout = proc.communicate()

				if proc.returncode == 1:
					print("Error")
					time.sleep(10)
					self.statusBar().showMessage("Error : AWS Credentials",3000)
					self.ui.submit_btn.setDisabled(False)
					self.ui.clear_btn.setDisabled(False)
				
				else:
					print("OK")
					time.sleep(10)
					self.ui.submit_btn.setDisabled(True)
					self.ui.clear_btn.setDisabled(True)
				

			else:
				self.ui.submit_btn.setDisabled(True)
				self.ui.clear_btn.setDisabled(True)
				print("Creating AWS Environment for {} user".format(getpass.getuser()))

				#Remove and Create the .aws directory
				os.system('rm -rf /home/'+getpass.getuser()+'/.aws')
				os.makedirs("/home/"+getpass.getuser()+"/.aws")

				#Creating AWS Credential file
				file_credential = open("/home/"+getpass.getuser()+"/.aws/credentials","w")
				file_credential.writelines("[default]\naws_access_key_id = {}\naws_secret_access_key = {}\n".format(self.ui.access_key_id_lineEdit.text(),self.ui.secret_access_key_lineEdit.text()))
				file_credential.close()

				#Create AWS Config file
				file_config = open("/home/"+getpass.getuser()+"/.aws/config","w")
				file_config.writelines("[default]\nregion={}\n".format(self.ui.region_lineEdit.text()))
				file_config.close()

				#Check the AWS Credentials
				

				aws_cred_cmd = "python3 /var/opt/PyQt-AWS-IAM/test_aws_credentials.py"
				proc = subprocess.Popen(aws_cred_cmd,stdout=subprocess.PIPE,shell=True)
				stdout = proc.communicate()

				if proc.returncode == 1:
					print("Error")
					time.sleep(5)
					self.statusBar().showMessage("Error : AWS Credentials",3000)
					self.ui.submit_btn.setDisabled(False)
					self.ui.clear_btn.setDisabled(False)
				
				else:
					print("OK")
					time.sleep(5)
					self.ui.submit_btn.setDisabled(False)
					self.ui.clear_btn.setDisabled(False)


	def clear_btn(self):

		print("Clear Button Clicked")

		#Clear all the fields
		self.ui.access_key_id_lineEdit.clear()
		self.ui.secret_access_key_lineEdit.clear()
		self.ui.region_lineEdit.clear()

		#Set Focus to Access Key ID
		self.ui.access_key_id_lineEdit.setFocus(True)


my_aws_iam_app = QtWidgets.QApplication([])
aws_iam = aws_iam_mainwindow()
aws_iam.show()
sys.exit(my_aws_iam_app.exec())		