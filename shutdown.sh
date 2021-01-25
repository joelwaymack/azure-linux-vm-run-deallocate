# Give a short timeout before deallocation.
sleep 10

# Login as VM managed identity
az login --identity

# Grab info to deallocate VM
resource_group=`az group list | grep name | awk '{ print $2 }' | grep -oP '"\K[^"\047]+(?=["\047])'`
vm_name=`hostnamectl | grep hostname | awk '{ print $3 }'`

# Deallocate VM
az vm deallocate -g $resource_group -n $vm_name