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

    $DIR/shutdown.sh&
fi