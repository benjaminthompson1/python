import struct

# Define a basic structure for the 'D' type record based on your layout.
# Modify these according to the actual lengths and types you need.
record_format = '29x44s1s1s2x2s1s1s1s1s1s1s2s6s2s2s4s4s4s4s4s4s8s32s32s32s32s2s2s8s8s1s1s2s4s32s16x'
record_size = struct.calcsize(record_format)

def read_dcollect_record(file_path):
    try:
        with open(file_path, 'rb') as file:
            while True:
                record_data = file.read(record_size)
                if not record_data:
                    break  # End of file

                # Unpack the record based on the defined format.
                record = struct.unpack(record_format, record_data)

                # Extract and display some fields. Adjust indexing based on added fields.
                dataset_name = record[0].strip().decode('utf-8')
                data_set_organization = record[6].hex()
                volume_serial_number = record[8].strip().decode('utf-8')
                block_length = int.from_bytes(record[9], byteorder='big', signed=False)
                record_length = int.from_bytes(record[10], byteorder='big', signed=False)

                # Display extracted information.
                print(f"Data Set Name: {dataset_name}")
                print(f"Data Set Organization: {data_set_organization}")
                print(f"Volume Serial Number: {volume_serial_number}")
                print(f"Block Length: {block_length}")
                print(f"Record Length: {record_length}")
                print("--------------------------------------------------")
    except FileNotFoundError:
        print("The file was not found. Please check the path and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Ask for the file path from the user.
file_path = input("Please enter the file location: ")
read_dcollect_record(file_path)
