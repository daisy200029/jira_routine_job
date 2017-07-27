from  jira_routine_job  import  *
import os
import re

# "C:\TestScripts\RobotFramework\\test_cases\web_portal\employer_group_manager"
class test_name_parser:
		def __init__(self,folder_name):
			self.test_name=[]
			self.ticket_id=[]
			self.test_data=[]
			self.test_result=[]
			self.test_id_now=""
			self.flag=False
			self.find_robot_file(folder_name)

		def find_robot_file(self,folder_name):
			for file in os.listdir(folder_name):
				if file.endswith(".robot"):
					self.flag=False
					file_path=os.path.join(folder_name,file)
					self.parse_test_name(file_path)

		def parse_test_name(self,file_path):
			with open(file_path) as  f:
				for  line  in iter(f):
					if line.startswith("${test_id}"):
						m=re.search('\d+',line.rstrip())
						self.test_id_now=m.group(0)
						# self.append_to_same_size()
					if line.startswith("*** Keywords ***"):
						self.flag=False
					if self.flag==True and not line.startswith(" ") and not line=='\n':
						self.collect_test_name(line.rstrip())
						self.collect_test_id()
					if line.startswith("*** Test Cases ***"):
						self.flag=True

			print  self.test_name
			
			self.generate_empty_result_data()
			print  self.ticket_id


		def  collect_test_id(self):
			if len(self.ticket_id)==0:
				self.ticket_id.append('CHPS-'+self.test_id_now)
			elif len(self.test_name) >= len(self.ticket_id):
				for  i in  range(0,len(self.test_name)-len(self.ticket_id)):
					self.ticket_id.append('CHPS-'+self.test_id_now)

		def  collect_test_name(self,line):
			self.test_name.append(line)

		def generate_empty_result_data(self):
			for  i in  range(0,len(self.test_name)):
				self.test_data.append("")
				self.test_result.append("")

if __name__ == "__main__":
	folder_name="C:\TestScripts\RobotFramework\\test_cases\web_portal\employer_group_manager"
	# find_robot_file("C:\TestScripts\RobotFramework\\test_cases\web_portal\employer_group_manager")
	parser1=test_name_parser(folder_name)
	# parser1.find_robot_file(folder_name)
	# parser1.parse_test_name("C:\TestScripts\RobotFramework\\test_cases\web_portal\employer_group_manager\CHPS4426_search_employer_group.robot")
	# find_robot_file()
	print parser1.test_name
	print parser1.ticket_id
	jira_name='dliu'
	jira_password='@WSX3edc'
	routine=jira_routine(jira_name,jira_password)
	tickets_id=routine.post_zephyr_teststep(ticket=parser1.ticket_id,test_step=parser1.test_name,test_data=parser1.test_data,test_result=parser1.test_result)