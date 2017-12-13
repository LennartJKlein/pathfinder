import subprocess

# Amount of netlist files
for i in range(1):
    
    # Netlist lengths (has to start at 2)
    for j in range(2, 3):

        command = "python pathfinder 50 0 " + str(j) +  " " + str(i)
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True).strip()

        print(output.decode('ascii'))