# Overview
This script allows you to run a command on an Azure VM with a Managed Identity and then deallocate the VM.

# Prequisites
1. The VM must have a Managed Identity associated with it. [Configure Managed Identity](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/qs-configure-portal-windows-vm)
1. The Managed Identity must an RBAC role that allows for VM deallocation such as Virtual Machine Contributor in the Resource Group or Subscription. [Add Role Assignment](https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal#add-a-role-assignment-for-a-managed-identity-preview)
1. SSH into the machine
    1. Run the setup.sh script.
    1. Copy the run.sh into a well-known location and ensure it has proper execution rights.

# Running
You can utilize this script multiple ways.

## Ad-hoc usage
1. Go into the Azure portal to the VM and choose `Operations > Run command > RunShellScript`.
1. Using the location of the script, run [script-location]/run.sh [your-command]
    * e.g. /home/me/run.sh echo "Hello, world!"
    * If you anticipate your command taking longer than 90 minutes, you will need to launch it as a separate process using `&`.
    * e.g. /home/me/run.sh echo "Hello, world!"&

## Azure Automation Scheduling
1. Go to an Azure Automation account and create a Python 3 Runbook with the code in runbook.py.
1. Add a schedule for the Runbook.
1. Include 3 parameters for the scheduled job:
    1. The Resource Group the VM is in.
    1. The VM's name.
    1. The script location and command to run.
        * Note the runbook will wait for execution of the command unless you use `&` to launch it as a separate process.
        * e.g. /home/me/run.sh sleep 60&