# CMSC 12300: Computer Science with Applications III Project
Team Members: Xi Chen, Yangyang Dai, Rose Gao, Liqiang Yu

## Folders & Files
- code: contains all python files
- notebooks: contains all notebooks
- presentation: contains the final presentation PowerPoint
- proposal: contains our initial project proposal
- report: contains our final report
- data: contains several smaller datasets and inputs for python files
- results: contains some sample outputs and results

## Usage
- friends_recommender.py
	- Run in command line: python3 friends_recommender.py --jobconf mapreduce.job.reduces=1 input_file > output_file
	- e.g. input_file = data/small.txt

- run_MRBFS.py
	- Run in command line: python3 run_MRBFS.py start_node end_node 
	- e.g. start_node = 902, end_node = 222

- get_pairs_distance.py
	- Run in command line: python3 get_pairs_distance.py -r dataproc --num-core-instances 4 input_file --file data_10000-20000.txt > output_distance_10000-20000.txt
	- e.g. input_file = data_10000-20000.txt

- closeness_centrality.py
	- Run in command line: python3 closeness_centrality.py input_file –file output_distance_10000-20000.txt > output_closeness_centrality.txt
	- e.g. input_file = user_10000-20000_community.txt

- degree_centrality.py
	- Run in command line: python3 degree_centrality.py -r dataproc --num-core-instances 4 data_input_file –file user_input_file > output_degree_centrality.txt
	- e.g. data_input_file = data_10000-20000.txt
	- e.g. user_input_file = user_10000-20000_community.txt
	
- eigenvector_centrality.py
	- Run in command line: python3 eigenvector_centrality.py input_file –file  > output_file
	- e.g. input_file = user_10000-20000_community.txt
	
- compute_all_paths.py
	- Run in command line: python3 compute_all_paths.py node_start node_end range_start range_end
	- e.g. node_start = 102, node_end = 367, range_start = 102, range_end = 367

- MRMinEccenticity.py
	- Run in command line: python3 MRMinEccentricity.py --jobconf mapreduce.job.reduces=1 input_file
	- e.g. input_file = ./results/paths.txt


## GCP Usage
python3 FriendsRecommender.py -r dataproc --num-core-instances 12 ./data/friends-000______.txt --output-dir=GCP_bucket_link

python3 FriendsRecommender.py --jobconf mapreduce.job.reduces=1 ./data/friends-000______small.csv 

python3 FriendsRecommender.py -r dataproc --instance-type n1-highmem-2 --num-core-instances 30 gs://mrjob-us-central1-ab479002dcab930f/data/friends-000______.txt --output-dir=GCP_bucket_link

python3 FriendsRecommender.py -r dataproc --num-core-instances 3 gs://mrjob-us-central1-ab479002dcab930f/data/friends-000______small.txt > 000_small.txt
