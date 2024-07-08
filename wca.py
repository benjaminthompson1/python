# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-20b-code-instruct-v2                 
import os
import re

def read_and_print_hzs_messages(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return

    # Regular expression to match HZSnnnnE or HZSnnnnW
    hzs_pattern = re.compile(r'HZS\d{4}[EW]')

    try:
        with open(file_path, 'r') as file:
            for line in file:
                match = hzs_pattern.search(line)
                if match:
                    print(line.strip())
    except IOError as e:
        print(f"Error reading the file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# File path
file_path = "/dsfs/txt/ibmuser/syslog.outputd"

# Call the function to read and print HZS messages
read_and_print_hzs_messages(file_path)                                                  