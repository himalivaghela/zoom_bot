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

def get_start_end_pairs_for_all(data):
    all_pairs = []
    
    for index, person in enumerate(data):
        start_times = person.get('start', [])
        end_times = person.get('end', [])
        
        # Create pairs of start and end times
        pairs = [[start, end] for start, end in zip(start_times, end_times)]
        
        # Add to the list with index for reference
        all_pairs.append({
            'name': person.get('name', f'Person {index}'),
            'pairs': pairs
        })
    
    return all_pairs

# Get start and end pairs for all persons
all_persons_pairs = get_start_end_pairs_for_all(json_data['data'])
print(type(all_persons_pairs))

print((all_persons_pairs[0]['pairs'][0]))

### Print the pairs for each person
##for person in all_persons_pairs:
##    print(f"Start and End Pairs for {person['name']}:")
##    for pair in person['pairs']:
##        print(pair)
##    print()  # Print a blank line between persons

##def separate_timestamps(data):
##    # Dictionary to store start and end times for each person
##    person_timestamps = {}
##    
##    # Iterate over each person in the data
##    for index, person in enumerate(data):
##        person_name = person.get('name', f'Person {index}')
##        start_times = person.get('start', [])
##        end_times = person.get('end', [])
##        
##        # Store start and end times in the dictionary
##        person_timestamps[person_name] = {
##            'start_times': start_times,
##            'end_times': end_times
##        }
##
##    return person_timestamps
##
### Get separate timestamps for each person
##timestamps_by_person = separate_timestamps(json_data['data'])
##
### Print the timestamps for each person
##for person_name, times in timestamps_by_person.items():
##    print(f"{person_name}:")
##    print(f"  Start Times: {times['start_times']}")
##    print(f"  End Times: {times['end_times']}")
