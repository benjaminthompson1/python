import struct

# Define constants for record types, assuming these short codes are in EBCDIC and need conversion
RECORD_TYPES = {
    b'\xc4@': 'ACTIVE DATA SET INFORMATION',          # 'D '
    b'\xc1@': 'VSAM BASE CLUSTER ASSOCIATION INFORMATION',  # 'A '
    b'\xe5@': 'VOLUME INFORMATION',                  # 'V '
    b'\xd4@': 'MIGRATED DATA SET INFORMATION',       # 'M '
    b'\xc2@': 'BACKUP DATA SET INFORMATION',         # 'B '
    b'\xc3@': 'DASD CAPACITY PLANNING INFORMATION',  # 'C '
    b'\xe3@': 'TAPE CAPACITY PLANNING INFORMATION',  # 'T '
    b'\xc4\xc3': 'DATA CLASS CONSTRUCT DEFINITION',  # 'DC'
    b'\xe2\xc3': 'STORAGE CLASS CONSTRUCT DEFINITION',  # 'SC'
    b'\xd4\xc3': 'MANAGMENT CLASS CONSTRUCT DEFINITION',  # 'MC'
    b'\xe2\x87': 'STORAGE GROUP CONSTRUCT DEFINITION',    # 'SG'
    b'\xe5\xd4': 'SMS VOLUME DEFINITION',            # 'VL'
    b'\xc2\xc3': 'BASE CONFIGURATION DEFINITION',    # 'BC'
    b'\xc1\x87': 'AGGREGATE GROUP DEFINITION',       # 'AG'
    b'\xc4\xd9': 'OPTICAL DRIVE DEFINITION',         # 'DR'
    b'\xd3\x82': 'OPTICAL LIBRARY DEFINITION',       # 'LB'
    b'\xc3\xd5': 'CACHE NAMES DEFINITION',           # 'CN'
    b'\xc1\xc9': 'ACCOUNTING INFORMATION DEFINITION', # 'AI'
}

def read_header(file):
    # Read RDW
    rdw = file.read(4)
    if not rdw or len(rdw) < 4:
        return None  # End of file or incomplete RDW

    # Unpack RDW to get the length of the record
    (length,) = struct.unpack('>H', rdw[0:2])

    # Check for incomplete file read or end of file
    if length <= 4:
        return None

    # Read the rest of the record based on the length
    record_data = file.read(length - 4)

    # Ensure we have read the expected amount of data
    if len(record_data) != length - 4:
        return None  # Incomplete record

    # Process each field in the header
    try:
        # Decoding EBCDIC character fields using code page 037
        dcu_length, dcu_rctype, dcu_vers, dcu_sysid = struct.unpack('>2x2s2s4s', record_data[0:10])
        record_type = dcu_rctype.decode('cp037')
        system_id = dcu_sysid.decode('cp037')
        version = int.from_bytes(dcu_vers, byteorder='big', signed=False)

        # Translate record type
        record_type_description = RECORD_TYPES.get(record_type.encode('cp037'), 'UNKNOWN')
    except struct.error:
        return None  # Unable to unpack the data, possibly due to an incomplete record

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
            break  # End of file or incomplete record reached
        print(header)
