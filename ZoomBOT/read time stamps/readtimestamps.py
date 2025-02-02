import json

# Open the JSON file and load the data
with open('trial.json', 'r') as file:
    json_data = json.load(file)

# Now you can access the data
##print(data)

number_of_persons = len(json_data['data'])

print(f"Number of persons in the JSON data: {number_of_persons}")
index = 0
person_name_at_index = json_data['data'][index]['name']
print(person_name_at_index)
def calculate_and_check_durations(data):
    # Store the durations and indices
    durations = []
    
    # Create a dictionary to map end times to their index
    end_time_to_index = {}
    for index, person in enumerate(data):
        end_times = person.get('end', [])
        for end_time in end_times:
            end_time_to_index[end_time] = index

    # Calculate durations and check for matches
    for index, person in enumerate(data):
        start_times = person.get('start', [])
        end_times = person.get('end', [])
        person_durations = []
        
        for start_time, end_time in zip(start_times, end_times):
            duration = round((end_time - start_time) / 10, 2)
            # Check if this start time is an end time of any other person
            if start_time in end_time_to_index:
                # Append index and duration
                person_durations.append([index, duration])
                
        if person_durations:
            durations.extend(person_durations)

    return durations

# Get the durations list
durations_list = calculate_and_check_durations(json_data['data'])
print(durations_list)

##def get_all_times(data):
##    all_timestamps = []
##
##    # Iterate over each person in the JSON data
##    for index, person in enumerate(data):
##        person_name = person['name']
##        timestamps = []
##
##        # Get start and end times for the person
##        start_times = person.get('start', [])
##        end_times = person.get('end', [])
##
##        # Calculate the duration between each start and end time
##        for start, end in zip(start_times, end_times):
##            duration = round((end - start) / 10, 2)
##            timestamps.append([index, duration])
##
##        # Store timestamps with person's index
##        all_timestamps.append({
##            'index': index,
##            'name': person_name,
##            'timestamps': timestamps
##        })
##
##    return all_timestamps
##
### Get the timestamps for all persons
##all_person_timestamps = get_all_times(data['data'])
##print(all_person_timestamps)

##
##def get_times_for_person(data, person_name):
##    # Iterate over each person in the JSON data
##    timestamps = []
##    # timestamps = [index,endtime-starttime]
##
##    for person in data:
##        if person['name'] == person_name:
##            # If the person's name matches, return their start and end times
##            start_times = person['start']
##            end_times = person['end']
##            
##    for start, end in zip(start_times, end_times):
##                duration = round((end - start) / 10,2)
##                t = [index,duration]
##                timestamps.append(t)
##    return timestamps
##    
##
### Extract start and end times for "Sudarshan ChavanKhot"
##t = get_times_for_person(data['data'], person_name_at_index)
##print(t)
