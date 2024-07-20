import re
from datetime import datetime, timedelta
from typing import List, Dict, Union

def parse_syslog_record(record: str) -> Dict[str, Union[str, List[str]]]:
    record_type = record[1].strip()
    task = record[38:46].strip()
    
    if record_type in {'D', 'E', 'S'}:
        return {
            "record_type": record_type,
            "system_identifier": "",
            "date": "",
            "time": "",
            "task": task,
            "message": record[55:].strip()
        }
    else:
        system_identifier = record[11:15].strip()
        julian_date = record[20:25].strip()
        timestamp = record[26:38].strip()
        message = record[55:].strip()

        date_str = parse_julian_date(julian_date)
        time_str = parse_timestamp(timestamp)

        return {
            "record_type": record_type,
            "system_identifier": system_identifier,
            "date": date_str,
            "time": time_str,
            "task": task,
            "message": message
        }

def parse_julian_date(julian_date: str) -> str:
    try:
        year = int(julian_date[:2])
        day_of_year = int(julian_date[2:])
        year += 2000 if year < 70 else 1900
        date = datetime(year, 1, 1) + timedelta(days=day_of_year - 1)
        return date.strftime('%Y-%m-%d')
    except ValueError:
        return 'Invalid Date'

def parse_timestamp(timestamp: str) -> str:
    try:
        time = datetime.strptime(timestamp, '%H:%M:%S.%f')
        return time.strftime('%H:%M:%S.%f')[:-4]  # Keep only two decimal places for seconds
    except ValueError:
        return 'N/A'

def process_syslog_file(file_path: str) -> List[Dict[str, Union[str, List[str]]]]:
    syslog_data = []
    current_multiline_message = None

    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():  # Check if the line is not empty
                record = parse_syslog_record(line)
                if record["record_type"] == "M":
                    if current_multiline_message:
                        syslog_data.append(current_multiline_message)
                    current_multiline_message = record
                    current_multiline_message["message"] = [record["message"]]
                elif record["record_type"] in {"D", "E", "S"}:
                    if current_multiline_message:
                        current_multiline_message["message"].append(record["message"])
                        if record["record_type"] == "E":
                            syslog_data.append(current_multiline_message)
                            current_multiline_message = None
                    else:
                        # Handle 'S' type as continuation of a single-line message
                        if syslog_data and record["record_type"] == "S":
                            syslog_data[-1]["message"] += " " + record["message"]
                        else:
                            syslog_data.append(record)
                else:
                    if current_multiline_message:
                        syslog_data.append(current_multiline_message)
                        current_multiline_message = None
                    syslog_data.append(record)

    if current_multiline_message:
        syslog_data.append(current_multiline_message)

    return syslog_data

def filter_records_by_type(syslog_data: List[Dict[str, Union[str, List[str]]]], record_type: str) -> List[Dict[str, Union[str, List[str]]]]:
    return [record for record in syslog_data if record['record_type'] == record_type]

def display_records(records: List[Dict[str, Union[str, List[str]]]]) -> None:
    for record in records:
        time_str = record['time']
        message = "\n".join(record['message']) if isinstance(record['message'], list) else record['message']
        print(f"{record['record_type']} {record['system_identifier']} {record['date']} {time_str} {record['task']}\n{message}\n")

def main() -> None:
    syslog_file_path = '/dsfs/txt/ibmuser/syslog.outputd'  # Update with your SYSLOG file path

    syslog_data = process_syslog_file(syslog_file_path)
    
    for record_type in ['X', 'N', 'M', 'W']:
        records = filter_records_by_type(syslog_data, record_type)
        print(f"\nRecords of type '{record_type}':")
        display_records(records)

if __name__ == "__main__":
    main()