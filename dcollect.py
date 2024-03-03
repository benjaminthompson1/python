import struct
import codecs

# Define constants for record types
RECORD_TYPES = {
    'D ': 'ACTIVE DATA SET INFORMATION',
    'A ': 'VSAM BASE CLUSTER ASSOCIATION INFORMATION',
    'V ': 'VOLUME INFORMATION',
    'M ': 'MIGRATED DATA SET INFORMATION',
    'B ': 'BACKUP DATA SET INFORMATION',
    'C ': 'DASD CAPACITY PLANNING INFORMATION',
    'T ': 'TAPE CAPACITY PLANNING INFORMATION',
    'DC': 'DATA CLASS CONSTRUCT DEFINITION',
    'SC': 'STORAGE CLASS CONSTRUCT DEFINITION',
    'MC': 'MANAGEMENT CLASS CONSTRUCT DEFINITION',
    'SG': 'STORAGE GROUP CONSTRUCT DEFINITION',
    'VL': 'SMS VOLUME DEFINITION',
    'BC': 'BASE CONFIGURATION DEFINITION',
    'AG': 'AGGREGATE GROUP DEFINITION',
    'DR': 'OPTICAL DRIVE DEFINITION',
    'LB': 'OPTICAL LIBRARY DEFINITION',
    'CN': 'CACHE NAMES DEFINITION',
    'AI': 'ACCOUNTING INFORMATION DEFINITION',
}

# Function to decode EBCDIC encoded data
def ebcdic_to_ascii(ebcdic_str):
    return codecs.decode(ebcdic_str, 'cp037')

def read_header(file):
    print("Reading RDW...")
    rdw = file.read(4)
    if not rdw or len(rdw) < 4:
        print("Incomplete or missing RDW. Ending read operation.")
        return None  # End of file or incomplete RDW

    # Unpack RDW to get the length of the record
    (length,) = struct.unpack('>H', rdw[0:2])
    print(f"RDW indicates record length: {length}")

    if length <= 4:
        print("RDW length less than or equal to 4. Invalid record length.")
        return None

    # Read the rest of the record based on the length
    record_data = file.read(length - 4)
    print(f"Read {len(record_data)} bytes from record data.")

    # Ensure we have read the expected amount of data
    if len(record_data) != length - 4:
        print("Incomplete record. Data read does not match RDW length.")
        return None  # Incomplete record

    # Process each field in the header
    try:
        print("Unpacking header data...")
        header_data = record_data[0:10]
        dcu_length, dcu_rctype, dcu_vers, dcu_sysid = struct.unpack('>2x2s2s4s', header_data)
    except struct.error as e:
        print(f"Error unpacking header: {e}")
        return None  # Unable to unpack the data, possibly due to an incomplete record

    # Decode EBCDIC encoded fields
    record_type = ebcdic_to_ascii(dcu_rctype)
    system_id = ebcdic_to_ascii(dcu_sysid)
    print(f"Decoded record type: {record_type}, system ID: {system_id}")

    # Convert version from binary
    version = int.from_bytes(dcu_vers, byteorder='big', signed=False)
    print(f"Decoded version: {version}")

    # Translate record type
    record_type_description = RECORD_TYPES.get(record_type.strip(), 'UNKNOWN')
    print(f"Record type description: {record_type_description}")

    # Return a dictionary of the header fields
    return {
        'length': length,
        'record_type': record_type.strip(),
        'record_type_description': record_type_description,
        'version': version,
        'system_id': system_id.strip(),
    }

# Prompt user for the DCOLLECT dataset file path
file_path = input("Please enter the path to the DCOLLECT dataset file: ")

# Process the specified file
with open(file_path, 'rb') as file:
    while True:
        header = read_header(file)
        if header is None:
            print("No more headers to read or an error occurred.")
            break  # End of file or incomplete record reached
        print(header)
