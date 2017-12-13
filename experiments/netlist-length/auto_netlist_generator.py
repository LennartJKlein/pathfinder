import subprocess

for i in range(80,101):
	command = "python generate_netlists.py " + str(i) + " 100 51"
	output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
	print(output)
