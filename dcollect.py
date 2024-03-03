import struct

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
    'MC': 'MANAGMENT CLASS CONSTRUCT DEFINITION',
    'SG': 'STORAGE GROUP CONSTRUCT DEFINITION',
    'VL': 'SMS VOLUME DEFINITION',
    'BC': 'BASE CONFIGURATION DEFINITION',
    'AG': 'AGGREGATE GROUP DEFINITION',
    'DR': 'OPTICAL DRIVE DEFINITION',
    'LB': 'OPTICAL LIBRARY DEFINITION',
    'CN': 'CACHE NAMES DEFINITION',
    'AI': 'ACCOUNTING INFORMATION DEFINITION',
}

def read_header(file):
    # Read RDW
    rdw = file.read(4)
    if not rdw:
        return None  # End of file

    # Unpack RDW to get the length of the record
    (length,) = struct.unpack('>H', rdw[0:2])

    # Read the rest of the record based on the length
    record_data = file.read(length - 4)

    # Process each field in the header
    dcu_length, dcu_rctype, dcu_vers, dcu_sysid = struct.unpack('>2x2s2s4s', record_data[0:10])
    dcu_tmstp = record_data[10:18]  # Timestamp is in packed decimal format and needs special handling

    # Convert record type, system ID, and version
    record_type = dcu_rctype.decode('utf-8')
    system_id = dcu_sysid.decode('utf-8')
    version = int.from_bytes(dcu_vers, byteorder='big')

    # Translate record type
    record_type_description = RECORD_TYPES.get(record_type, 'UNKNOWN')

    # Return a dictionary of the header fields
    return {
        'length': length,
        'record_type': record_type,
        'record_type_description': record_type_description,
        'version': version,
        'system_id': system_id,
        # The timestamp requires more sophisticated decoding if needed.
    }

# Example usage
file_path = 'your_dataset.dcollect'
with open(file_path, 'rb') as file:
    while True:
        header = read_header(file)
        if header is None:
            break  # End of file reached
        print(header)
