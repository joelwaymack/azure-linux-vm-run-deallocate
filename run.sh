echo "****** Script Started ******"
echo `date`
if [ $# -eq 0 ]
then
    echo "No commands given."
else
    echo "Command: $@"
    $@
    echo "Command executed."

    ./shutdown.sh&
fi