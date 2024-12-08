#!/bin/zsh

# Print a message indicating what the script will do
echo "Deleting .bak and .log files from the current directory..."

# Delete all .bak and .log files in the current directory
rm -v *.bak *.log 2>/dev/null

# Check if files were deleted successfully
if [[ $? -eq 0 ]]; then
  echo "All .bak and .log files have been deleted."
else
  echo "No .bak or .log files found or an error occurred."
fi
