import struct
import json
import codecs
import sys

def ebcdic_to_ascii(ebcdic_bytes):
    return codecs.decode(ebcdic_bytes, 'cp1047')

def read_dcollect_record(file):
    # Read record length (first 2 bytes)
    length_bytes = file.read(2)
    if not length_bytes:
        return None  # End of file
    
    record_length = struct.unpack('>H', length_bytes)[0]
    print(f"Debug: Record length read: {record_length}")
    
    if record_length <= 2:
        print(f"Error: Invalid record length: {record_length}")
        return None
    
    # Read the rest of the record
    try:
        record_data = file.read(record_length - 2)
    except ValueError as e:
        print(f"Error reading record data: {e}")
        return None
    
    # Parse record type (assuming it's in the first byte after length)
    record_type = struct.unpack('>B', record_data[:1])[0]
    
    return record_type, record_data

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
                
                # Simple parsing example - adjust based on actual DCOLLECT record formats
                parsed_record = {
                    'record_type': record_type,
                    'data': ebcdic_to_ascii(record_data[1:])
                }
                
                json_data.append(parsed_record)
                
                if record_count % 1000 == 0:
                    print(f"Processed {record_count} records")
        
        print(f"Total records processed: {record_count}")
        
        # Write JSON data to file
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