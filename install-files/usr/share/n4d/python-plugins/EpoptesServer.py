import subprocess
import os
import n4d.server.core as n4dcore
import n4d.responses
import tempfile
import netifaces

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


	
	def release_ip(self,ipserver_netcard,var_epoptes_ip_sever):
		
		try:
			print("Deleting obsolete Ip EpoptesServer: %s"%ipserver_netcard)
			#command="ip addr del %s/24 dev %s"%(ipserver_netcard[0],ipserver_netcard[1])
			command="natfree-iface unset"
			print(command)
			t=os.system(command)
			if t=="0":
				self.core.set_variable(var_epoptes_ip_sever,None)
				return n4d.responses.build_successful_call_response(True)
			else:
				return n4d.responses.build_successful_call_response(False)
		except Exception as e:
			return n4d.responses.build_failed_call_response('',str(e))
	#def release_ip
	


class EpoptesServer:
	
	def __init__(self):
		pass
		#self.allowed_ips=set()
		#self.del_epoptes_from_iptables()
		#self.set_drop_epoptes()
		
	#def init
	
	'''
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
	'''
	
	'''
	def register_ip(self,ip):
		
		self.allowed_ips.add(ip)
		self.set_epoptes_in_iptables()
		#Old n4d: return True
		return n4d.responses.build_successful_call_response()
		
	#def register_ip
	'''


	def set_ip_server(self,ipserver):
		
		try:
			'''
			print('Discovering Eth in use.....')
			eth_used=self.discover_eth()
			print('ETH_USED: %s'%eth_used)
			if eth_used!=None:
				print("Adding new Ip EpoptesServer: %s"%ipserver)
				command="ip addr add %s/24 dev %s"%(ipserver,eth_used)
				print(command)
				os.system(command)
				return n4d.responses.build_successful_call_response(eth_used)
			else:
				return n4d.responses.build_failed_call_response()
		except Exception as e:
			return n4d.responses.build_failed_call_response()
			'''

			print('Adding Ip/mask to Virtual ETH')
			command="natfree-iface set %s"%(ipserver)
			t=os.system(command)
			if t=="0":
				return n4d.responses.build_successful_call_response(True)
			else:
				return n4d.responses.build_successful_call_response(False)
		except Exception as e:
			return n4d.responses.build_failed_call_response()
		
	#def set_ip_server



	def discover_eth (self):
		try:
			x=netifaces.interfaces()
			netcard_used=None
			print(x)
			for i in x:
				if i != 'lo':
					print('testing %s'%i)
					try:
						ip = netifaces.ifaddresses(i)[netifaces.AF_INET][0]['addr']
						print('IP addr: {0} '.format(ip))
						netcard_used=i
						print('Netcard in use: %s'%netcard_used)
					except KeyError:
						print('NO IP')
						continue
			return netcard_used
		except Exception as e:
			print('Exception discover_eth %s'%e)
			return n4d.responses.build_failed_call_response('',str(e))
	#def_discover_eth



	def ip_free(self,ipserver):
		
		return n4d.responses.build_successful_call_response(True)
		
	#def ip_free

	
	
	'''def set_drop_epoptes(self):
		
		cmd="iptables -A INPUT -p tcp --dport 10000 -j DROP"
		#print(cmd)
		os.system(cmd)
		
	#def_ip_free
	'''
	
	
	'''def set_epoptes_in_iptables(self):
		
		self.del_epoptes_from_iptables()
			
		for item in self.allowed_ips:
			
			cmd="iptables -A INPUT -p tcp --dport 10000 -s %s -j ACCEPT"%item
			#print(cmd)
			os.system(cmd)
			
		

		self.set_drop_epoptes()
		
		#Old n4d: return True
		return n4d.responses.build_successful_call_response()

		
	#def set_iptables'''


	'''def list_iptables (self):

		try:
			tmp = tempfile.NamedTemporaryFile()
			file=tmp.name
			cmd="iptables -L FORWARD | grep DROP | awk '{ print $4 }' > %s"%file
			os.system(cmd)
			f = open(file)
			lines = f.read().splitlines()
			f.close()
			return n4d.responses.build_successful_call_response([True,lines])
				
		except Exception as e:
			#Old n4d: return [False,str(e)]
			if os.path.exists(file):
				if os.path.isfile(file):
					os.remove(file)
			return n4d.responses.build_failed_call_response('',str(e))


	#def list_iptables'''
	
	
#class EpoptesServer


if __name__=="__main__":
	
	es=EpoptesServer()
	es.register_ip("10.2.1.189")
	es.parse_iptables()
