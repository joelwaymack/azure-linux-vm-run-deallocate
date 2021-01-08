echo "********************"
echo "** Run & Shutdown **"
echo "********************"


if [ $# -eq 0 ]
then

    echo "No commands given."
    echo "Skipping deallocation."

else

    $@

    # Login as VM managed identity
    az login --identity

    # Grab info to deallocate VM
    resource_group=`az group list | jq -r '.[0].name'`
    vm_name=`hostnamectl | grep hostname | awk '{ print $3 }'`

    # Deallocate VM
    az vm deallocate -g $resource_group -n $vm_name

fi