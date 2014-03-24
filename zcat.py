"""
ZCAT, Send multiple files over your network!
=============================================
renjith 2014, renjithforever@gmail.com
license: use as u like on your own risk!

___+[ABOUT]+_______
nc or NETCAT is a cool linux tool that can send files over your network.
Howerver it doesnt allow u to send multiple files, in which case you have
to tar/compress the files.

ZCAT bridges this gap by allowing you to send multiple files in one go!
ZCAT uses nc!

__+[REQUIREMNTS]+_____
python, nc, therefore linux!

__+[USAGE]+____
sender must start zcat first, inform the receiver ur IP
and start zcat at the receivers end!

send files:
	python zcat.py -s <path-to-folder>

receive files:	
	python zcat.py -r <host-ip>

interactive mode:
	python zcat.py


"""
import subprocess
import os
import re
import sys
import socket


def zcat_send_record(record_fileName,portNum):
	command="nc -l "+str(portNum)+" <"+record_fileName
	process=subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)
	process.wait()

def zcat_send_files(record,initPortNum):
		
	for portNum,fileName in record.items():
		
		command="nc -l "+str(portNum)+" <"+fileName
		process=subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)

def zcat_get_record(record_fileName,host,portNum):
		
	
	dummy=open(record_fileName,"w")
	dummy.write('')
	dummy.close()


	command="nc "+str(host)+" "+str(portNum)+" >"+record_fileName

	process=subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)
	process.wait()

	record_obj=open(record_fileName,"r")
	record={}
	message=record_obj.readline()

	if message=='':
		sys.exit("[!] NOTHING TO RECEIVE")

	for line in record_obj:
		line=line.strip().split(":")
		portNum=line[0]
		fileName=line[1]
		record[portNum]=fileName

	return message,record

def zcat_get_files(record,host):

	for portNum,fileName in record.items():
		fileName=fileName.split("/")[-1]
		fileName='"'+fileName
		print fileName,
		sys.stdout.flush()
		command="nc "+host+" "+str(portNum)+" >"+fileName
		process=subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)
		process.wait()
		print "...done!"



def make_record(path,initPortNum,record_fileName="record",message="file list..."):
	"""
	"""

	files=[]
	for _,dirs,fileName in os.walk (path):
		if '.git' in dirs:
			dirs.remove('.git')
		if 'test' in dirs:
			dirs.remove('test')
		files.extend(fileName)

	record={}
	portNum=initPortNum

	record_obj=open(record_fileName,"w")

	record_obj.write(message+'\n')
	selectAll=raw_input("[#] SELECT ALL FILES IN "+path+' (y/n)\n[<<] ')
	selectAll=True if selectAll in ['yes','YES','y','Y',''] else False

	for file in files:

		if file == record_fileName or file[0]=='.' or '.py' in file:
			continue

		file=path+file
		file='"'+file+'"'

		print "[#] file: ",file
		if not selectAll:
			prompt=raw_input("[#] SELECT? (y/n)\n[<<] ")
			prompt='no' if prompt in ['n','N','NO','no'] else 'yes'
			if prompt=='no':
				continue

		record[portNum]=file
		record_obj.write(str(portNum)+":"+file+'\n')
		portNum+=1


	record_obj.close()

	return record

	



def get_params():
	action=''
	path=''
	host=''
	message="file list..."
	port=1200
	CURSOR_UP_ONE = '\x1b[1A'
	ERASE_LINE = '\x1b[2K'


	if len(sys.argv)>1:
		if sys.argv[1]=='-s':
			action='SEND'
			if len(sys.argv)>2:
				path=sys.argv[2]
			else:
				path='./'
		elif sys.argv[1]=='-r':
			action="RECEIVE"
			if len(sys.argv)>2:
				host=sys.argv[2]
			else:
				print "provide host"
				sys.exit()
		pass
	else:
		action=raw_input("[#] SEND or RECEIVE?\n[<<] ")
		action = "SEND" if (action in ['SEND','send','s','S']) else "RECEIVE"
		print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
		print "[<<]",action
		if action == "SEND":
			path=raw_input("[#] SOURCE FOLDER? \n[<<] ")
			if path =='':
				path='./'
			elif path[-1]!='/':
				path+='/'
			else:
				pass
			
			print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
			print "[<<]",path
			path=path+'/' if path[-1] != '/' else path
			port=raw_input("[#] PORT? (default=1200) \n[<<]")
			port = 1200 if (port =='' or int(port)<=1000) else int(port)

			print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
			print "[<<]",port
			message=raw_input("[#] MESSAGE? \n[<<] ")
			message="hi.. i am sending u these" if message == '' else message
			print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
			print "[<<]",message

			ip=get_machine_ip()
			print "[#] YOUR IP:",ip,"(pass this to the receiver)"
		else:
			host=raw_input("[#] HOST IP? \n[<<] ")
			host = "localhost" if host=='' else host

			print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
			print "[<<]",host
			port=raw_input("[#] PORT? (default=1200) \n[<<]")
			port = 1200 if (port =='' or int(port)<=1000) else int(port)
			print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
			print "[<<]",port



	return action,path,port,host,message


	
def show_record(record):
	for fileName in record.values():
		print fileName.split("/")[-1], '\t',

	print ""
	

def get_machine_ip():
	"""
	"""

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	IP=(s.getsockname()[0])
	s.close()
	return IP

if __name__ == "__main__":

	action,path,port,host,message=get_params()
	init_port=port

	
	if action=='SEND':
		record=make_record(path,init_port,"record",message)
		print "[#] WAITING FOR RECIEVER TO CONNECT!"
		zcat_send_record("record",init_port)
		print "[#] FILE LIST SENT"
		zcat_send_files(record,init_port+1)
		print "[note] COMPLETION WILL NOT BE ACKNOWLEDGED!"
		pass
	else:
		print "[#] CONNECTING..."
		message,record=zcat_get_record("record",host,init_port)
		print "\n[MESSAGE]:",message,'\n'
		print "[#] FILES TO BE RECEIVED\n"
		show_record(record)

		prompt=raw_input("\n[#] RECEIVE THESE FILES? (y/n): \n[<<] ")
		if prompt=='y':
			zcat_get_files(record,host)
			print  TRANSFER COMPLETE!"
		else:


			pass
