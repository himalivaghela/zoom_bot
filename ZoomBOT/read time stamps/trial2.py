import json

# Open the JSON file and load the data
with open('trial.json', 'r') as file:
    json_data = json.load(file)

# Function to get start and end pairs for all persons
def get_start_end_pairs_for_all(data):
    all_pairs = []
    
    for index, person in enumerate(data):
        start_times = person.get('start', [])
        end_times = person.get('end', [])
        
        # Create pairs as dictionaries
        pairs = [{'start': start, 'end': end} for start, end in zip(start_times, end_times)]
        
        # Add to the list with index for reference
        all_pairs.append({
            'name': person.get('name', f'Person {index}'),
            'pairs': pairs
        })
    
    return all_pairs

# Get start and end pairs for all persons
all_persons_pairs = get_start_end_pairs_for_all(json_data['data'])
a=0
# Check for overlaps between end times and start times of different persons
for i in range(len(all_persons_pairs)):
    for j in range(len(all_persons_pairs[i]['pairs'])):
        end_time_i = all_persons_pairs[i]['pairs'][j]['end']
        
        for k in range(len(all_persons_pairs)):
            if k != i:  # Ensure we are not comparing the same person
                for l in range(len(all_persons_pairs[k]['pairs'])):
                    start_time_k = all_persons_pairs[k]['pairs'][l]['start']
                    
                    # Check for overlap
                    if end_time_i >= start_time_k:
                        print(f"End time of {all_persons_pairs[i]['name']} (index {i}) overlaps with start time of {all_persons_pairs[k]['name']} (index {k})")
                        a=a+1
                        print(a)
                        break  # Exit the loop if an overlap is found


##import json
##
### Open the JSON file and load the data
##with open('trial.json', 'r') as file:
##    json_data = json.load(file)
##
### Now you can access the data
####print(data)
##
##number_of_persons = len(json_data['data'])
##
##print(f"Number of persons in the JSON data: {number_of_persons}")
##index = 0
##person_name_at_index = json_data['data'][index]['name']
##print(person_name_at_index)
##
##def get_start_end_pairs_for_all(data):
##    all_pairs = []
##    
##    for index, person in enumerate(data):
##        start_times = person.get('start', [])
##        end_times = person.get('end', [])
##        
##        # Create pairs of start and end times
##        pairs = [[start, end] for start, end in zip(start_times, end_times)]
##        
##        # Add to the list with index for reference
##        all_pairs.append({
##            'name': person.get('name', f'Person {index}'),
##            'pairs': pairs
##        })
##    
##    return all_pairs
##
### Get start and end pairs for all persons
##all_persons_pairs = get_start_end_pairs_for_all(json_data['data'])
####print(len(all_persons_pairs))
####
######print((all_persons_pairs[0]['pairs'][0]))
####print(len(all_persons_pairs[1]['pairs']))
##l_p = []
##for i in range(len(all_persons_pairs)):
##    len_pairs = len(all_persons_pairs[i]['pairs'])
##    l_p.append(len_pairs)
##
### Get start and end pairs for all persons
##all_persons_pairs = get_start_end_pairs_for_all(json_data['data'])
##
### Check for overlaps between end times and start times of different persons
##for i in range(len(all_persons_pairs)):
##    for j in range(len(all_persons_pairs[i]['pairs'])):
##        end_time_i = all_persons_pairs[i]['pairs'][j]['end']
##        for k in range(len(all_persons_pairs)):
##            if k != i:  # Ensure we are not comparing the same person
##                for l in range(len(all_persons_pairs[k]['pairs'])):
##                    start_time_k = all_persons_pairs[k]['pairs'][l]['start']
##                    if end_time_i >= start_time_k:
##                        print(f"End time of {all_persons_pairs[i]['name']} (index {i}) overlaps with start time of {all_persons_pairs[k]['name']} (index {k})")


                        
##print(l_p)
##a = 0
##for i in range(len(l_p)):
##    a = 0
##    while (a < l_p[i]):
##        st = all_persons_pairs[i]['pairs'][a]
##        start_time = all_persons_pairs[i]['pairs'][a][0]
##        end_time = all_persons_pairs[i]['pairs'][a][1]
##        
##        print(st)
##        a = a+1
##        
##    for j in range(l_p[i]):

##for i in range(len(all_persons_pairs)):
##    for j in range(len(all_persons_pairs[i]['pairs'])):
##        end_time_i = all_persons_pairs[i]['pairs'][j]['end']
##        for k in range(len(all_persons_pairs)):
##            if k != i:
##                for l in range(len(all_persons_pairs[k]['pairs'])):
##                    start_time_k = all_persons_pairs[k]['pairs'][l]['start']
##                    if end_time_i >= start_time_k:
##                        print(f"End time of person {i} overlaps with start time of person {k}")
##                        break


##    st = all_persons_pairs[0]['pairs'][i]
##    print(st)







