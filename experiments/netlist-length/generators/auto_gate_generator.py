import subprocess

for i in range(1,101):
	command = "python generate_gates.py " + str(i) + " 100 50"
	output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
	print(output)
