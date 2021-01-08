import sys

if len(sys.argv) < 4:
    exit('Missing required arguments!\nUsage: resource_group_name vm_name run_command')
else:
    resource_group_name = str(sys.argv[1])
    vm_name = str(sys.argv[2])
    run_command = str(sys.argv[3])

    for count in range (4, len(sys.argv)):
        run_command += ' ' + str(sys.argv[count])

    print('RG: ' + resource_group_name + '\nVM: ' + vm_name + '\nRun: ' + run_command)