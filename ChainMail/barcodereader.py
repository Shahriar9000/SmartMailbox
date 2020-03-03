import os, subprocess, sys, time

if os.path.exists('out.txt'):
	os.remove('out.txt')
rpistr = "raspistill -t 1000 -o image.jpg && zbarimg image.jpg >> out.txt"

p = subprocess.Popen(rpistr, shell=True, preexec_fn=os.setsid)
time.sleep(3)
if os.path.exists('out.txt'):
	with open("out.txt", "r") as file:
		inputx = file.readline()

        print(inputx)
