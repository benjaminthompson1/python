#!/usr/bin/env python3                               
import zoautil_py.datasets as Datasets               
import sys                                           
                                                     
if len(sys.argv) != 3:                               
   print('Please provide source and destination datasets')         
   sys.exit()                                        
                                                     
dsn1 = sys.argv[1]  # Source dataset                              
dsn2 = sys.argv[2]  # Destination dataset

dsn1_data = Datasets.read(dsn1)  # Read data from source dataset

print("Source Dataset (dsn1): ", dsn1)
print("Data being copied: \n", dsn1_data)

check = Datasets.exists(dsn2)  # Check if the destination dataset exists                   
if check:                                            
   Datasets.delete(dsn2)  # If it does, delete it

Datasets.create(dsn2,"SEQ","record_format=FB")  # Create the new dataset

Datasets.write(dsn2, dsn1_data)  # Write the data from dsn1 to dsn2

dsn2_data = Datasets.read(dsn2)  # Read data from destination dataset
print("Destination Dataset (dsn2): ", dsn2)
print("Data in destination dataset: \n", dsn2_data)
