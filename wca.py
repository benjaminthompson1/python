# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-20b-code-instruct-v2
import zoautil_py as zoautil

# Define the input dataset name
dataset_name = 'IBMUSER.SYSLOG.OUTPUTD'

# Open the input dataset
dataset = zoautil.Dataset(dataset_name)

# Read the contents of the dataset line by line
for record in dataset:
    # Process each record
    print(record)

# Close the dataset
dataset.close()