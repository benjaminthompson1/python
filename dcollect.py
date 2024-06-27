import struct
import json
import codecs

def ebcdic_to_ascii(ebcdic_bytes):
    return codecs.decode(ebcdic_bytes, 'cp1047')

def read_dcollect_record(file):
    length_bytes = file.read(2)
    if not length_bytes:
        return None  # End of file
    record_length = struct.unpack('>H', length_bytes)[0]
    print(f"Debug: Record length read: {record_length}")
    
    if record_length <= 2:
        print(f"Error: Invalid record length: {record_length}")
        return None
    
    record_data = file.read(record_length - 2)
    record_type = struct.unpack('>B', record_data[:1])[0]
    
    return record_type, record_data

def parse_dcollect_record(record_type, record_data):
    parsed_record = {
        'record_type': record_type,
        'record_type_name': get_record_type_name(record_type)
    }
    
    parse_functions = {
        0: parse_type_0,
        212: parse_type_212,
        220: parse_type_220
    }
    
    parse_function = parse_functions.get(record_type)
    if parse_function:
        try:
            parsed_record.update(parse_function(record_data))
        except Exception as e:
            print(f"Error parsing record type {record_type}: {e}")
            parsed_record['parsing_error'] = str(e)
    else:
        parsed_record['data'] = ebcdic_to_ascii(record_data[1:])
    
    return parsed_record

def get_record_type_name(record_type):
    record_types = {
        0: 'Header',
        1: 'Active Data Set',
        2: 'Non-VSAM',
        3: 'VSAM Base Cluster',
        4: 'VSAM Alternate Index',
        5: 'VSAM Path',
        6: 'Generation Data Set',
        7: 'Guaranteed Space',
        8: 'Rolled-off GDS',
        9: 'VSAM Volume',
        10: 'SMS Volume Status',
        11: 'SMS Storage Group',
        12: 'SMS Management Class',
        13: 'SMS Data Class',
        14: 'SMS Storage Class',
        15: 'Total DASD Capacity',
        16: 'SMS Bound Data Class',
        17: 'SMS Bound Management Class',
        18: 'SMS Bound Storage Class',
        19: 'Volume',
        20: 'Migrated Data Set',
        21: 'Tape Capacity',
        22: 'Tape Volume',
        23: 'Data Set Error',
        24: 'DASD Volume Error',
        25: 'SMS Storage Group Error',
        26: 'Coupling Facility (CF) Cache Structure',
        27: 'Coupling Facility (CF) Lock Structure',
        212: 'VVDS Information',
        220: 'Data Set Backup'
    }
    return record_types.get(record_type, 'Unknown')

def parse_type_0(record_data):
    # Header record
    return {
        'system_id': ebcdic_to_ascii(record_data[6:14]).strip(),
        'time_stamp': struct.unpack('>Q', record_data[14:22])[0],
        'sms_level': ebcdic_to_ascii(record_data[22:30]).strip()
    }

def parse_type_212(record_data):
    # VVDS Information
    return {
        'volume_serial': ebcdic_to_ascii(record_data[6:12]).strip(),
        'device_number': ebcdic_to_ascii(record_data[12:18]).strip(),
        'vvds_name': ebcdic_to_ascii(record_data[18:62]).strip(),
        'component_code': struct.unpack('>H', record_data[62:64])[0],
        'number_of_ci': struct.unpack('>I', record_data[64:68])[0],
        'ci_size': struct.unpack('>H', record_data[68:70])[0]
    }

def parse_type_220(record_data):
    # Data Set Backup
    return {
        'dsname': ebcdic_to_ascii(record_data[6:50]).strip(),
        'volume_serial': ebcdic_to_ascii(record_data[50:56]).strip(),
        'backup_version_gen': struct.unpack('>I', record_data[56:60])[0],
        'backup_version_date': struct.unpack('>I', record_data[60:64])[0],
        'backup_version_time': struct.unpack('>I', record_data[64:68])[0]
    }

def process_dcollect(input_file, output_file):
    json_data = []
    
    try:
        with open(input_file, 'rb') as f:
            record_count = 0
            while True:
                record = read_dcollect_record(f)
                if record is None:
                    break
                
                record_type, record_data = record
                record_count += 1
                
                parsed_record = parse_dcollect_record(record_type, record_data)
                json_data.append(parsed_record)
                
                if record_count % 1000 == 0:
                    print(f"Processed {record_count} records")
        
        print(f"Total records processed: {record_count}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2)
        
    except IOError as e:
        print(f"Error opening or reading file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Main execution
if __name__ == "__main__":
    input_file = "/dsfs/txt/IBMUSER/dcollect"
    output_file = "/u/ibmuser/dcollect.json"
    
    print(f"Starting DCOLLECT processing")
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    
    process_dcollect(input_file, output_file)
    print(f"Conversion complete. JSON data written to {output_file}")