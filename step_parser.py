from  jira_routine_job  import  *
import logging
import os

class  step_parser:
		def __init__(self, file_path):
			self.test_step=[]
			self.test_data=[]
			self.test_result=[]
			self.test_tickets=[]
			self.flag=-1
			self.step=""
			self.data=""
			self.result="" 
			self.ticket="" 
			self.parse_file(file_path)

			print  self.test_step
			print  self.test_data
			print  self.test_result
			print  self.test_tickets


		def  check_step_key(self, line):
			if self.flag == 1:
				self.ticket+=line
			elif self.flag== 2 :
				line+="\n"
				self.step+=line
			elif self.flag== 3 :
				line+="\n"
				self.data+=line
			elif self.flag== 4 :	
				line+="\n"
				self.result+=line

		def  check_content_exist(self):		
			if  self.step != "":
				self.test_step.append(self.step)
				self.step = ""
			if  self.data != "":
				self.test_data.append(self.data)
				self.data = ""
			if  self.result != "":
				self.test_result.append(self.result)
				self.result=""
			if  self.ticket != "":
				self.test_tickets.append(self.ticket)
				self.ticket=""


		def parse_file(self,file_path):
			with open(file_path) as  f:
				for  line  in iter(f):
					line =line.rstrip()
					if line.startswith('@ticket') or line.startswith('@step') or line.startswith('@data') or line.startswith('@result')or line.startswith('!exit'):
						if line.startswith('@ticket'):
							self.check_content_exist()
							self.flag=1
						elif line.startswith('@step'):
							self.check_content_exist()
							self.flag=2
						elif line.startswith('@data'):
							self.check_content_exist()
							self.flag=3
						elif line.startswith('@result'):
							self.check_content_exist()
							self.flag=4
						else :
							self.check_content_exist()
					else:
						self.check_step_key(line)
			
			if  len(self.test_data)<len(self.test_step):
				size_diff=len(self.test_step)-len(self.test_data)
				for i in range (0,size_diff):
					self.test_data.append("")
				print "append null to test_data to match the size"
			if len(self.test_step) != len(self.test_result) or len(self.test_result)==0 or len(self.test_step)==0:
				raise  "test step size is not match with test result size"
				# raise "test_step size %d and test data result %d len not matches" % ( len(test_step), len(test_result))



if __name__ == "__main__":
		file_path=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'uploads', 'step.txt')
		parser1=step_parser(file_path)


