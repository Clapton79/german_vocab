#!/bin/zsh

# Print a message indicating what the script will do
echo "Deleting .bak and .log files from the current directory..."

# Delete all .bak and .log files in the current directory
rm -v *.bak 
rm -v *.log 
