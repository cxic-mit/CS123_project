# Friendster Network Analysis
## Project for CMSC 12300: Computer Science with Applications III 

Team Name: The Da Vinci Code

Team Members: Xi Chen, Yangyang Dai, Rose Gao, Liqiang Yu

We would like to express our sincere gratitude to Dr. Matthew Wachs for his support on this project!

## Introduction
The purpose of this project is to serve as a grounding framework for social network analysis with big data. Our project uses the Friendster’s dataset from the Stanford SNAP data collection. 

## Folders & Files
- code: 
	- Community Analysis:
		- betweenness_centrality.py
		- closeness_centrality.py
		- comm.py
		- degree_centrality.py
		- eigenvector_centrality.py
		- find_comm_50.py
		- find_shortest_path.py
		- get_pairs_distance.py
	- Network Analysis:
		- compute_all_paths.py
		- friends_recommender.py
		- MRBFS.py
		- MRMinEccentricity.py
		- run_MRBFS.py

- notebooks:
	- De-Anonymization.ipynb: this notebook explores de-anonymizing the friend lists of private users; ultimately we decided not to implement a MapReduce algorithm because only 9 out of 1,000,000 users in our small dataset were de-anonymized
	- Exploration.ipynb: initial exploration for project
	- NetworkX_Comparison.ipynb: comparing all community centrality measures and friends recommender against our MapReduce algorithms

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
	- Run in command line: python3 get_pairs_distance.py input_file --file copy_file > output_distance.txt
	- e.g. input_file = data_10000-20000.txt
	- e.g. copy_file = data_10000-20000.txt
	
- find_comm_50.py
	- Run in command line: python3 find_comm_50.py input_file > output_community.txt
	- e.g. input_file = output_distance.txt
	- e.g. output_file = output_community.txt
	
- find_comm.py
	- same as above
	- the only difference is the format of the data in the output file
	
- closeness_centrality.py
	- Run in command line: python3 closeness_centrality.py input_file --file distance_file > output_closeness_centrality.txt
	- e.g. input_file = user_10000-20000_community.txt
	- e.g. distance_file = output_distance_10000-20000.txt

- degree_centrality.py
	- Run in command line: python3 degree_centrality.py input_file --file community_file > output_degree_centrality.txt
	- e.g. input_file = data_10000-20000.txt
	- e.g. community_file = user_10000-20000_community.txt
	
- eigenvector_centrality.py
	- Run in command line: python3 eigenvector_centrality.py community_file --file input_file > output_file
	- e.g. community_file = user_1000-2000_community.txt
	- e.g. input_file = data_1000-2000.txt
	
- compute_all_paths.py
	- Run in command line: python3 compute_all_paths.py node_start node_end range_start range_end
	- e.g. node_start = 102, node_end = 367, range_start = 102, range_end = 367

- MRMinEccenticity.py
	- Run in command line: python3 MRMinEccentricity.py --jobconf mapreduce.job.reduces=1 input_file
	- e.g. input_file = ./results/paths.txt


## GCP Usage
python3 friends_recommender.py -r dataproc --num-core-instances 12 ./data/friends-000______.txt --output-dir=GCP_bucket_link

python3 friends_recommender.py -r dataproc --instance-type n1-highmem-2 --num-core-instances 30 ./data/friends-000______.txt --output-dir=GCP_bucket_link

python3 friends_recommender.py -r dataproc --num-core-instances 3 gs://mrjob-us-central1-ab479002dcab930f/data/friends-000______small.txt > 000_small.txt

python3 get_pairs_distance.py -r dataproc --num-core-instances 4 data_10000-20000.txt --file data_10000-20000.txt > output_distance_10000-20000.txt

python3 degree_centrality.py -r dataproc --num-core-instances 4 data_10000-20000.txt --file user_10000-20000_community.txt > output_degree_centrality.txt


