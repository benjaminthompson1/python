import json
from zoautil_py import datasets

# Read the DCOLLECT dataset
with datasets.DD(name="IBMUSER.DCOLLECT", mode="rb") as infile:
    dcollect_data = infile.read().decode("utf-8")

# Parse the DCOLLECT data into a list of dictionaries
dcollect_records = []
for line in dcollect_data.splitlines():
    record = {}
    # Parse each line and populate the record dictionary
    # Adjust the parsing logic based on the DCOLLECT output format
    # Example parsing:
    record["volume"] = line[0:6].strip()
    record["unit"] = line[6:10].strip()
    # ... parse other fields ...
    dcollect_records.append(record)

# Convert the DCOLLECT records to JSON format
json_data = json.dumps(dcollect_records, indent=2)

# Write the JSON data to a new dataset
output_dsname = "IBMUSER.DCOLLECT.JSON"
with datasets.DD(name=output_dsname, mode="wb") as outfile:
    outfile.write(json_data.encode("utf-8"))

print(f"DCOLLECT data converted to JSON and written to dataset: {output_dsname}")