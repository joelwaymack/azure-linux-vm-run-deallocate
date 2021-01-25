echo "****** Script Started ******"
echo `date`
if [ $# -eq 0 ]
then
    echo "No commands given."
else
    echo "Command: $@"
    $@
    echo "Command executed."

    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

    echo "Shutting down in 10 seconds..."
    $DIR/shutdown.sh&
fi