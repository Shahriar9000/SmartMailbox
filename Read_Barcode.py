import os
import re
from subprocess import Popen, PIPE
import time


def If_Barcode(output):
    pattern = re.compile(r"(CODE-128)|(EAN-13)|(EAN-8)|(EAN-2)|(EAN-5)|(UPC-A)|(UPC-E)|(ISBN-10)|(ISBN-13):[0-9]+")
    matches = re.match(pattern, output)
    if matches:
    	return True
    else:
    	return False

def excute_command(command):
	system = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
	system_info = system.communicate()
	if system_info[0]:
		stdout = system_info[0].strip('\n')
		return stdout
	if system_info[1]:
		stderr = system_info[1]
		return stderr

	return False


def get_Barcode():
    GetBarcode = "ssh pi@192.168.43.127 python barcodereader.py"
    timeout = time.time() + 60*5  # 5 minutes from now
    while True:
        system = Popen(GetBarcode, shell=True, stdout=PIPE, stderr=PIPE)
        system_info = system.communicate()
        print(system_info[0])
        print(system_info[1])
        output = system_info[0].strip('\n')
        if If_Barcode(output):
            Barcode = output
            return Barcode
            break;
        if time.time() > timeout:
            print('Failed to read barcode for 5 minutes')
            exit(1)


	


def Main():
	output = excute_command("ssh pi@192.168.43.127 uname -a")
	print(output)
	Barcode = get_Barcode()
	print(Barcode)



	

	

if __name__ == '__main__':
	Main()