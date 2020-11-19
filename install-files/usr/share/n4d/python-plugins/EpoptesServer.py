import subprocess
import os

class EpoptesVariables:

	
	def __init__(self):
		pass
		
	#def __init__
	
	def add_group(self,n4d_mode=None):
		
		try:
		
			import xmlrpclib as x
			c=x.ServerProxy("https://server:9779")
			VALOR=c.get_variable(n4d_mode,"VariablesManager","EPOPTES_GROUPS")
			#print ("VALOR VARIABLE EPOPTES_GROUPS %s" %VALOR)
			if  VALOR==None:
				objects["VariablesManager"].add_variable("EPOPTES_GROUPS",{},"","Epoptes Groups",[],False,False)
				#print c.add_variable(n4d_mode,"VariablesManager","EPOPTES_GROUPS",{},"","Epoptes Groups",[],False,False)
				COMMENT = "[EpoptesVariables] Added variable EPOPTES_GROUPS to VariablesManager"
				print ("%s" %COMMENT)
				return [True,str(COMMENT)]
			else:
				COMMENT="[EpoptesVariables] EPOPTES_GROUPS Variable exists in your system, it hasn't been created again"
				return [True,str(COMMENT)]
		except Exception as e:
			return [False,str(e)]
		
	#def add_group
	
	
	def set_group(self,n4d_mode=None,data=None):
		
		try:
		
			import xmlrpclib as x
			c=x.ServerProxy("https://server:9779")
			objects["VariablesManager"].set_variable("EPOPTES_GROUPS",data)
			#c.set_variable(n4d_mode,"VariablesManager","EPOPTES_GROUPS",data)
			COMMENT="[EpoptesVariables] EPOPTES_GROUPS has been updated"
			print ("%s" %COMMENT)
			return [True,str(COMMENT)]
				
		except Exception as e:
			return [False,str(e)]
		
	#def set_group
	


class EpoptesServer:
	
	def __init__(self):
		
		self.allowed_ips=set()
		self.del_epoptes_from_iptables()
		self.set_drop_epoptes()
		
	#def init
	
	def del_epoptes_from_iptables(self):
		
		p=subprocess.Popen(["iptables-save"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		output=p.communicate()[0].split("\n")
		
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
		return True
		
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
		
		return True
		
	#def set_iptables
	
	
#class EpoptesServer


if __name__=="__main__":
	
	es=EpoptesServer()
	es.register_ip("10.2.1.189")
	es.parse_iptables()
