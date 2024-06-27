import struct
import json
import codecs

def ebcdic_to_ascii(ebcdic_bytes):
    return codecs.decode(ebcdic_bytes, 'cp1047')

def read_dcollect_record(file):
    # Read record length (first 2 bytes)
    length_bytes = file.read(2)
    if not length_bytes:
        return None  # End of file
    record_length = struct.unpack('>H', length_bytes)[0]
    
    # Read the rest of the record
    record_data = file.read(record_length - 2)
    
    # Parse record type (assuming it's in the first byte after length)
    record_type = struct.unpack('>B', record_data[:1])[0]
    
    return record_type, record_data

def process_dcollect(input_file, output_file):
    json_data = []
    
    with open(input_file, 'rb') as f:
        while True:
            record = read_dcollect_record(f)
            if record is None:
                break
            
            record_type, record_data = record
            
            # Simple parsing example - adjust based on actual DCOLLECT record formats
            parsed_record = {
                'record_type': record_type,
                'data': ebcdic_to_ascii(record_data[1:])  # Remove the .decode() call here
            }
            
            json_data.append(parsed_record)
    
    # Write JSON data to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)

# Main execution
if __name__ == "__main__":
    input_file = "/dsfs/txt/IBMUSER/dcollect"
    output_file = "/u/ibmuser/dcollect.json"
    process_dcollect(input_file, output_file)
    print(f"Conversion complete. JSON data written to {output_file}")