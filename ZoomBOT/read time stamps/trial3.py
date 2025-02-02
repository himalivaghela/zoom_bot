import json

# Open the JSON file and load the data
with open('trial.json', 'r') as file:
    json_data = json.load(file)



# Initialize a counter for overlaps
overlap_count = 0

def check_overlaps(data):
    overlap_count = 0

    for i in range(len(data)):
        for j in range(len(data[i]['start'])):
            # Get Sudarshan's end time
            end_time_sudarshan = data[i]['end'][j]

            # Check against all other persons
            for k in range(len(data)):
                if k != i:  # Ensure we are not comparing the same person
                    for l in range(len(data[k]['start'])):
                        start_time_dheeraj = data[k]['start'][l]

                        # Check if Sudarshan's end time matches Dheeraj's start time
                        if end_time_sudarshan == start_time_dheeraj:
                            print(f"End time of {data[i]['name']} (index {i}) matches start time of {data[k]['name']} (index {k})")

                            # Check if Dheeraj's times overlap with Sudarshan's
                            for m in range(len(data[k]['start'])):
                                start_time_dheeraj = data[k]['start'][m]
                                end_time_dheeraj = data[k]['end'][m]

                                # Check if Dheeraj's end time matches Sudarshan's start time
                                if end_time_dheeraj == data[i]['start'][j]:
                                    print(f"End time of {data[k]['name']} (index {k}) matches start time of {data[i]['name']} (index {i})")
                                    overlap_count += 1
                                    print(f"Overlap count increased to: {overlap_count}")

    return overlap_count

# Execute the function
overlap_count = check_overlaps(json_data['data'])

print(f"Total overlaps found: {overlap_count}")
