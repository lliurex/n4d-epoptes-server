import subprocess
import os
import n4d.server.core as n4dcore
import n4d.responses

class EpoptesVariables:

	
	def __init__(self):

		self.core=n4dcore.Core.get_core()
		pass
		
	#def __init__
	
	def add_group(self,n4d_mode=None):
		
		try:
			'''
			import xmlrpclib as x
			c=x.ServerProxy("https://server:9779")
			VALOR=c.get_variable(n4d_mode,"VariablesManager","EPOPTES_GROUPS")
			'''
			VALOR=self.core.get_variable("EPOPTES_GROUPS").get('return',None)
			#print ("VALOR VARIABLE EPOPTES_GROUPS %s" %VALOR)
			if  VALOR==None:
				#Old n4d: objects["VariablesManager"].add_variable("EPOPTES_GROUPS",{},"","Epoptes Groups",[],False,False)
				self.core.set_variable("EPOPTES_GROUPS",{})
				#print c.add_variable(n4d_mode,"VariablesManager","EPOPTES_GROUPS",{},"","Epoptes Groups",[],False,False)
				COMMENT = "[EpoptesVariables] Added variable EPOPTES_GROUPS to VariablesManager"
				print ("%s" %COMMENT)
				#Old n4d:return [True,str(COMMENT)]
				return n4d.responses.build_successful_call_response('',str(COMMENT))
			else:
				COMMENT="[EpoptesVariables] EPOPTES_GROUPS Variable exists in your system, it hasn't been created again"
				#Old n4d:return [True,str(COMMENT)]
				return n4d.responses.build_successful_call_response('',str(COMMENT))

		except Exception as e:
			#Old n4d: return [False,str(e)]
			return n4d.responses.build_failed_call_response('',str(e))
		
		
	#def add_group
	
	
	def set_group(self,n4d_mode=None,data=None):
		
		try:
			'''
			import xmlrpclib as x
			c=x.ServerProxy("https://server:9779")
			objects["VariablesManager"].set_variable("EPOPTES_GROUPS",data)
			'''
			self.core.set_variable("EPOPTES_GROUPS",data)
			#c.set_variable(n4d_mode,"VariablesManager","EPOPTES_GROUPS",data)
			COMMENT="[EpoptesVariables] EPOPTES_GROUPS has been updated"
			print ("%s" %COMMENT)
			#Old n4d: return [True,str(COMMENT)]
			return n4d.responses.build_successful_call_response('',str(COMMENT))
				
		except Exception as e:
			#Old n4d: return [False,str(e)]
			return n4d.responses.build_failed_call_response('',str(e))

		
	#def set_group
	


class EpoptesServer:
	
	def __init__(self):
		
		self.allowed_ips=set()
		self.del_epoptes_from_iptables()
		self.set_drop_epoptes()
		
	#def init
	
	def del_epoptes_from_iptables(self):
		
		p=subprocess.Popen(["iptables-save"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		output=p.communicate()[0]

		if type(output) is bytes:
			output=output.decode()
			
		output=output.split("\n")
		
		ret=[]
		
		for item in output:
			if "--dport 10000" in item and "INPUT" in item:
				ret.append("iptables " + item.replace("-A","-D"))
		
		
		for item in ret:
			#print(item)
			os.system(item)
		
		
	#def parse_iptables
	
	def register_ip(self,ip):
		
		self.allowed_ips.add(ip)
		self.set_epoptes_in_iptables()
		#Old n4d: return True
		return n4d.responses.build_successful_call_response()
		
	#def register_ip
	
	def set_drop_epoptes(self):
		
		cmd="iptables -A INPUT -p tcp --dport 10000 -j DROP"
		#print(cmd)
		os.system(cmd)
		
	#
	
	
	def set_epoptes_in_iptables(self):
		
		self.del_epoptes_from_iptables()
			
		for item in self.allowed_ips:
			
			cmd="iptables -A INPUT -p tcp --dport 10000 -s %s -j ACCEPT"%item
			#print(cmd)
			os.system(cmd)
			
		

		self.set_drop_epoptes()
		
		#Old n4d: return True
		return n4d.responses.build_successful_call_response()

		
	#def set_iptables
	
	
#class EpoptesServer


if __name__=="__main__":
	
	es=EpoptesServer()
	es.register_ip("10.2.1.189")
	es.parse_iptables()
