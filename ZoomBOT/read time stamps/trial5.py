import json

# Open the JSON file and load the data
with open('trial.json', 'r') as file:
    json_data = json.load(file)

def compute_durations(data):
    result_list = []  # To store [duration, person] entries
    person_map = {}  # To quickly lookup start and end times by name
    visited_pairs = set()  # To store unique (person, duration) pairs to avoid repetitions

    # Step 1: Calculate durations and map them
    for person in data:
        name = person['name']
        start_times = person['start']
        end_times = person['end']
        durations = [round((end_times[i] - start_times[i])/10,2) for i in range(len(start_times))]

        # Store the person's times and durations
        person_map[name] = {'start': start_times, 'end': end_times, 'durations': durations}

    # Step 2: Find the chain of overlaps
    for i in range(len(data)):
        person = data[i]
        name = person['name']
        start_times = person_map[name]['start']
        end_times = person_map[name]['end']
        durations = person_map[name]['durations']

        # Iterate through each start-end pair for the person
        for j in range(len(start_times)):
            # Prepare the current pair for checking
            current_pair = (durations[j], name)

            # Add the initial person's duration to the result list if not already visited
            if current_pair not in visited_pairs:
                result_list.append(list(current_pair))
                visited_pairs.add(current_pair)

            # Get the end time of the current person to check for a match
            current_end_time = end_times[j]

            # Step 3: Check if current end time matches any other person's start time
            for k in range(len(data)):
                if data[k]['name'] != name:  # Avoid comparing the person with themselves
                    other_person = data[k]
                    other_name = other_person['name']
                    other_start_times = person_map[other_name]['start']
                    other_durations = person_map[other_name]['durations']

                    if current_end_time in other_start_times:
                        # Find the index where the match occurs
                        match_index = other_start_times.index(current_end_time)
                        matching_pair = (other_durations[match_index], other_name)

                        # Append the matching person's duration if not already visited
                        if matching_pair not in visited_pairs:
                            result_list.append(list(matching_pair))
                            visited_pairs.add(matching_pair)

                        # Update the current_end_time to the new person's end time for further chaining
                        current_end_time = person_map[other_name]['end'][match_index]

    return result_list

# Execute the function
result_list = compute_durations(json_data['data'])

print(len(result_list))
print("Result List with durations and person names:")
for item in result_list:
    print(item)
