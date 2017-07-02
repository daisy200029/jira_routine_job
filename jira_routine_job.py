##Refernce Zephyr API: http://docs.getzephyr.apiary.io/#reference/executionresource/create-new-execution/create-new-execution
##Reference JIRA Python Library  http://jira.readthedocs.io/en/master/api.html
from jira.client import JIRA
import cgi
import re
import urllib3
import requests
import sys

class jira_routine:

 		def __init__(self, jira_user, jira_password):
 			requests.packages.urllib3.disable_warnings()
	 		self.jira_user = jira_user
	 		self.jira_password = jira_password
	 		self.jira_server = 'https://jira.emdeon.net/'
	 		self.jira_project_key = 'CHPS'
	 		self.jira_authentication()
	 		self.get_web_portal_project_component()
	 		self.get_web_portal_project_version()
	 		self.get_npp_project_component()
	 		self.get_npp_project_version()
	 		self.get_npp_sprint_id()
	 		self.get_webportal_sprint_id()
	 		self.project_id="11404"	 		

 		def jira_authentication(self):
			options = {
			    'server': self.jira_server,
			    'verify': False
			}
			
			jira = JIRA(options, basic_auth=(self.jira_user, self.jira_password))
			self.jira=jira



		def  get_npp_sprint_id(self):
			# jira board number is 513
			sprints=self.jira.sprints(513)
			npp_sprint_id=sprints[-2].id
			self.npp_sprint_id=npp_sprint_id
			return  npp_sprint_id


		def  get_webportal_sprint_id(self):
			sprints=self.jira.sprints(513)
			web_portal_sprint_id=sprints[-3].id
			self.web_portal_sprint_id=web_portal_sprint_id
			return web_portal_sprint_id	 


		def  create_story_ticket_from_story(self,version,component, list_story_tickets=[]):
			output_story_tickets=[]
			for issue in list_story_tickets :
				summary=self.get_issue_summary(issue)
				story = {
				'project' : { 'key' : 'CHPS' },
				'summary' : 'QA--'+ summary,
				'description' : '',
				'issuetype' : { 'name' : 'Story' },
				'assignee' : { 'name' : self.jira_user},
				'labels': ['QA'],
				'fixVersions': [ {'name' : version }  ],
				'components':[{ 'name' : component } ]
				}
				story_ticket = self.jira.create_issue( fields= story)
				output_story_tickets.append(story_ticket.key)
			return  output_story_tickets


		def  create_test_ticket_from_story(self, version, component, list_story_tickets=[]):
			output_zephyr_tickets=[]
			for issue in list_story_tickets :
				summary=self.get_issue_summary(issue)
				zephyr = {
				'project' : { 'key' : 'CHPS' },
				'summary' : 'Automation Test '+summary,
				'description' : '',
				'issuetype' : { 'name' : 'Test' },
				'assignee' : { 'name' : self.jira_user},
				'labels': ['QA'],
				'fixVersions': [ {'name' : version }  ],
				'components':[{ 'name' : component } ]

				}
				zephyr_ticket = self.jira.create_issue( fields= zephyr)
				output_zephyr_tickets.append(zephyr_ticket.key)
			return  output_zephyr_tickets



		def create_subtask_from_story(self, list_story_tickets=[]):
			output_subtask_tickets=[]
			for issue in list_story_tickets :
				summary= self.get_issue_summary(issue)
				subtask = {
				'project' : { 'key' : 'CHPS' },
				'summary' : 'Automation Testing for '+summary,
				'description' : '',
				'issuetype' : { 'name' : 'Sub-task' },
				'parent' : { 'id' : issue},
				'assignee' : { 'name' : self.jira_user}
				}
				subtask_ticket = jira.create_issue(fields=subtask)
			output_subtask_tickets.append(subtask_ticket.key)
			return  output_subtask_tickets


		def get_issue_summary(self,issue):
			jiraissue = self.jira.issue(issue)
			summary=str(jiraissue.fields.summary)
			return  summary


		def add_issues_to_sprint(self, sprint_id ,list_tickets=[]):
			list_issue_id=[]
			for issue in list_tickets:
				jiraissue = self.jira.issue(issue)
				list_issue_id.append(jiraissue.id)
			self.jira.add_issues_to_sprint( sprint_id, list_issue_id)
			print  "successfully add to current sprint"


		def create_issue_link(self, parentkey, childkey ):
            # create jira issue link(outwardIssue:parent-issue,inwardIssue=child-issue )
			self.jira.create_issue_link(type="Derived",inwardIssue=childkey,
			outwardIssue=parentkey)
			print  "successfully create issue link"


		def get_sprints(self):
			sprints=self.jira.sprints(513)
			print sprints


		def create_bug(self, assignee, summary, description):		
			bugs = []
			for i in range (0, len(description)) :
				bug= {
					    'project': {'key': 'CHPS'},
					    'summary': summary[i],
					    'description': description[i],
					    'issuetype': { 'name' : 'Bug' },
					    'assignee' : { 'name' : assignee[i] },
					    'labels': ['QA']
					    # 'fixVersions': [ {'name' : version }  ],
						# 'components':[{ 'name' : component } ]
					}
				bugs.append(bug)
			issues = self.jira.create_issues(field_list=bugs)
			out = [ issue.get('issue') for issue in issues]
			print  out
			return  out
			# self.add_issues_to_sprint(sprint_id, out) 


		def get_web_portal_project_component(self):
			chps = self.jira.project(self.jira_project_key)
			components = self.jira.project_components(chps)
			out=[c.name for c in components]               
			self.webportal_project_component=out[-1]
			return out[-1]


		def get_web_portal_project_version(self):
			chps = self.jira.project(self.jira_project_key)
			versions = self.jira.project_versions(chps)
			out=[v.name for v in reversed(versions)]        
			self.webportal_project_version=out[-2]
			return out[-2]


		def get_npp_project_component(self):
			chps = self.jira.project(self.jira_project_key)
			components = self.jira.project_components(chps)
			out=[c.name for c in components]  
			self.npp_project_component=out[-3]
			return out[-3]


		def get_npp_project_version(self):
			chps = self.jira.project(self.jira_project_key)
			versions = self.jira.project_versions(chps)
			out=[v.name for v in reversed(versions)]
			self.npp_project_version=out[-1]
			return out[-1]


		def create_web_potal_test_and_story_based_on_story(self,version,component, list_story_tickets=[]):
			list_out_story=routine1.create_story_ticket_from_story(version, component, list_story_tickets)
			list_out_test=routine1.create_test_ticket_from_story(version, component, list_out_story)
			merge_list=list_out_story+list_out_test
			# self.add_issues_to_sprint(self.webportal_project_version, merge_list)
			size=len(list_out_story)
			for i in  range (0, size) :
				self.create_issue_link(list_out_story[i],list_out_test[i])
				self.create_issue_link(list_story_tickets[i],list_out_story[i])
			print merge_list


		def  add_attachment(self, ticket , filepath):
			jiraissue = self.jira.issue(ticket)
			self.jira.add_attachment(issue=jiraissue, attachment=filepath)
			print "successfully upload file attachment" 


		def get_zephyr_teststep(self,ticket):
			jiraissue = self.jira.issue(ticket)
			r = self.jira._session.get(self.jira_server+'/rest/zapi/latest/teststep/'+jiraissue.id, verify=False)
			print r.text
			print r.status_code


		def post_zephyr_teststep(self,ticket, test_step, test_data, test_result):
			for i in range (0, len(ticket)) :
				jiraissue = self.jira.issue(ticket[i])
				zephyrstep={
					  "step": test_step[i],
					  "data": test_data[i],
					  "result": test_result[i]
					}
				r = self.jira._session.post(self.jira_server+'/rest/zapi/latest/teststep/'+jiraissue.id,json=zephyrstep,verify=False)
				print r.status_code
				print "successfully post "
			return  ticket

		def get_cycle_information(self,cycle_id):
			r = self.jira._session.get(self.jira_server+'/rest/zapi/latest/cycle/'+cycle_id ,verify=False) 
			r =r.json()
			print r['name']
			print r['id']
		

		def create_cycle(self,data):
			r = self.jira._session.post(self.jira_server+'/rest/zapi/latest/cycle/',json=data,verify=False) 
			r =r.json()
			cycle_id=r['id']
			print "successfully create cycle "+cycle_id
			return cycle_id
			
		
		def delete_cycle_by_id(self,cycle_id):
			r = self.jira._session.delete(self.jira_server+'/rest/zapi/latest/cycle/'+cycle_id,verify=False) 
			print "successfully delete "+cycle_id
		

		def get_list_of_cycle(self):
			r = self.jira._session.get(self.jira_server+'/rest/zapi/latest/cycle?projectId='+self.project_id,verify=False)
			r= r.json()
			print r


		def get_list_of_execution_by_issuekey(self, ticket):
			jiraissue = self.jira.issue(ticket)
			r = self.jira._session.get(self.jira_server+'/rest/zapi/latest/execution?'+jiraissue.id,verify=False)
			r=r.json()
			print r


		def create_new_execution_with_status(self,ticket, cycle_id,status):
			jiraissue = self.jira.issue(ticket)
			data={
					  "cycleId": cycle_id,
					  "issueId": jiraissue.id ,
					  "projectId":self.project_id,
					  # "versionId": "10001",
					  "assigneeType": "assignee",
					  "assignee": self.jira_user
				}

			r = self.jira._session.post(self.jira_server+'rest/zapi/latest/execution',json=data,verify=False)
			r=r.json()
			execution_id=r.keys()[0] #only one id
			self.update_execution(execution_id, "1")
			print "successfully create new execution "+ str(execution_id) +"with status"+status


		def update_execution(self,execution_id,status):
			status={
					"status": status
				}

			r = self.jira._session.put(self.jira_server+'rest/zapi/latest/execution/'+execution_id+'/execute',json=status,verify=False)
			print "successfully update "+execution_id


		def delete_execution(self,execution_id):
			r = self.jira._session.delete(self.jira_server+'rest/zapi/latest/execution/'+execution_id,verify=False)
			r=r.json()
			# print "successfully delete "+execution_id
			print r


if __name__ == "__main__":
	username="your username"
	password="your password"
	routine1=jira_routine(username,password)
	# #==============================================================================================================================
	# #Create web portal test and story
	# tickets=["CHPS-1176"]
	# routine1.create_web_potal_test_and_story_based_on_story(version=\
	# 	routine1.webportal_project_version,component=routine1.webportal_project_component,list_story_tickets=tickets)
	# #==============================================================================================================================
	# #EX: create bug
	# routine1.create_bug(assignee_list, summary_list,description_list,routine1.web_portal_sprint_id, routine1.webportal_project_version, routine1.webportal_project_component)
	# #==============================================================================================================================
	# #EX: add attachment
	#routine1.add_attachment("CHPS-2981", 'test.pdf')
	# routine1.add_attachment("CHPS-2981", 'C:\\test.pdf')
	# #==============================================================================================================================
	# #EX: get zephyr teststp by ticket key
	# routine1.get_zephyr_teststep("CHPS-2007")
	# #==============================================================================================================================
	# EX:post zephr teststep by ticket key
	# routine1.post_zephyr_teststep(ticket="CHPS-2981",test_step=test_step_list, test_data=test_data_list, test_result=test_result_list)
	#==============================================================================================================================
	#EX:Create zephyr test cycle 
	# cycle={
	# 	  "clonedCycleId": "",
	# 	  "name": "Sprint15",
	# 	  "build": "",
	# 	  "environment": "",
	# 	  "description": "Create cycle with sprint15",
	# 	  "projectId": routine1.project_id,	
	# 	  "versionId": "-1"
	# 	}
	# cycle_id=routine1.create_cycle(cycle)
	# #==============================================================================================================================
	#EX:Get list of zephyr test cycle 
	# routine1.get_list_of_cycle()
	# #==============================================================================================================================
	# # #EX:Create Execution (cycle_id=-1 is ad_hoc, cycle_id=722 is sprint13)
	# # # #EX:Update execution status (1:pass 2:fail 3:WIP 4:Blocked 5: unexpected)	
	# routine1.create_new_execution_with_status(ticket="CHPS-2981",cycle_id=722,status="1")
	# # # #==============================================================================================================================
	# # #==============================================================================================================================
	# # #EX:delete execution
	# routine1.delete_execution(execution_id)
	# #==============================================================================================================================
	#EX:Delete zephyr test cycle by cycle id
	# routine1.delete_cycle_by_id("731")
	# # #==============================================================================================================================
	