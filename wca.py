# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-20b-code-instruct-v2
import zoslogs

# Specify the path to the log file
log_path = '/dsfs/txt/ibmuser/syslog.outputd'

# Create a ZosLogs object and pass the log file path
log = zoslogs.ZosLogs(log_path)

# Iterate over the log messages
for message in log:
    # Print the message ID, job ID (if available), and message text
    print(f"Message ID: {message.message_id}, Job ID: {message.job_id if message.job_id else 'N/A'}, Message: {message.message}")                               