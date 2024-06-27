// Assisted by WCA@IBM
// Latest GenAI contribution: ibm/granite-20b-code-instruct-v2
import struct
import os

def read_dcollect_record(file):
    # Read record descriptor word (RDW)
    rdw = file.read(4)
    if not rdw:
        return None
    
    record_length = struct.unpack('>H', rdw[:2])[0] - 4
    
    # Read the rest of the record
    record = file.read(record_length)
    
    return record

def parse_dcollect_record(record):
    # Parse record based on DCOLLECT format
    record_type = record[0:1].decode('ascii')
    
    if record_type == 'V':  # Volume record
        volser = record[6:12].decode('ascii').strip()
        total_space = struct.unpack('>I', record[24:28])[0]
        free_space = struct.unpack('>I', record[28:32])[0]
        
        return f"Volume: {volser}, Total Space: {total_space}, Free Space: {free_space}"
    
    elif record_type == 'D':  # Dataset record
        dsname = record[44:132].decode('ascii').strip()
        allocated_space = struct.unpack('>I', record[132:136])[0]
        
        return f"Dataset: {dsname}, Allocated Space: {allocated_space}"
    
    else:
        return f"Unsupported record type: {record_type}"

def process_dcollect_file(filename):
    with open(filename, 'rb') as file:
        while True:
            record = read_dcollect_record(file)
            if not record:
                break
            
            parsed_record = parse_dcollect_record(record)
            write_to_file(parsed_record)

def write_to_file(output):
    # Write output to a file
    output_file = '/u/ibmuser/output.txt'
    if not os.path.exists(output_file):
        with open(output_file, 'w') as file:
            file.write(output)
    else:
        with open(output_file, 'a') as file:
            file.write('\n' + output)

# Usage
process_dcollect_file('/dsfs/txt/IBMUSER/dcollect')
