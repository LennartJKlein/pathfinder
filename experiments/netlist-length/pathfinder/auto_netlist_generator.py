import subprocess

for i in range(2,51):
	command = "python generate_netlists.py " + str(i) + " 100 30" # amount-connections amount-files max-gate-number
	output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
	print(output)
