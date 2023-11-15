#!/bin/bash

# Define databases, cutoffs, and looseness values
databases=("players")  # Add your database values here
cutoffs=(1000 5000 10000)  # Add your cutoff values here
looseness_values=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0)  # Looseness values from 0.1 to 1 in steps of 0.1

# Get current time in the required format (dd-mm-yy-hh-mm)
current_time=$(date +'%d-%m-%y-%H-%M')

# Loop through combinations of database, cutoff, and looseness values
for database in "${databases[@]}"; do
    for cutoff in "${cutoffs[@]}"; do
            # Run the command for each combination of database, cutoff, and looseness
             # Formulate the command for each combination of database, cutoff, and looseness
            command="python3 main.py --notqdm --database \"$database\" --criterion bruteforce --cutoff \"$cutoff\" --utility-function '[0.8770164597139456, 0.4061596562468818, 0.27105740994353467, 0.5556577457210364, 0.5015490345149674, 0.2772325170286718, 0.3433570969047466, 0.8945670536948659, 0.33960561437443126, 0.624037718157554, 0.6782966998383805, 0.7433124521382295, 0.939705139604908, 0.1551337727082157, 0.7796439780242693, 0.022275101852821888, 0.30361071236525206, 0.014235479649710836, 0.6317392506273638, 0.4954480873235546]'"
            
            # Create a file to store the command
            echo "$command" > "experiments/log-bruteforce-${database}-${cutoff}-${looseness}-${current_time}.txt"

            # Display the command
            echo "Executing: $command"

            # Run the command for each combination of database, cutoff, and looseness
            eval "$command" &> "experiments/log-bruteforce-${database}-${cutoff}-${looseness}-${current_time}.txt"
        
        
        for looseness in "${looseness_values[@]}"; do
            # Run the command for each combination of database, cutoff, and looseness
             # Formulate the command for each combination of database, cutoff, and looseness
            command="python3 main.py --notqdm --database \"$database\" --criterion LP --looseness \"$looseness\" --cutoff \"$cutoff\" --utility-function '[0.8770164597139456, 0.4061596562468818, 0.27105740994353467, 0.5556577457210364, 0.5015490345149674, 0.2772325170286718, 0.3433570969047466, 0.8945670536948659, 0.33960561437443126, 0.624037718157554, 0.6782966998383805, 0.7433124521382295, 0.939705139604908, 0.1551337727082157, 0.7796439780242693, 0.022275101852821888, 0.30361071236525206, 0.014235479649710836, 0.6317392506273638, 0.4954480873235546]'"
            
            # Create a file to store the command
            echo "$command" > "experiments/log-LP-${database}-${cutoff}-${looseness}-${current_time}.txt"

            # Display the command
            echo "Executing: $command"

            # Run the command for each combination of database, cutoff, and looseness
            eval "$command" &> "experiments/log-LP-${database}-${cutoff}-${looseness}-${current_time}.txt"
        done
    done
done
