# CMSC 12300: Computer Science with Applications III Project
Team Members: Xi Chen, Yangyang Dai, Rose Gao, Liqiang Yu

Folders & Files:
- Code (contains all of our codes)
- Presentation (contains the PPT for the final presentation)
- Proposal (contains our initial proposed project)
- Report (contains our final report)
- data (contains several small sample data and input for the files)
- Results (contains some sample outputs/results)

Usage: 
- FriendsRecommender.py
	- Run in command line: python3 FriendsRecommender.py --jobconf mapreduce.job.reduces=1 data/small.txt > data/output.txt

- Get_pairs_distance.py
	- Run in command line: python3 Get_pairs_distance.py -r dataproc --num-core-instances 4 data_10000-20000.txt --file data_10000-20000.txt > output_distance_10000-20000.txt

- Closeness_centrality.py
	- Run in command line: python3 Closeness_centrality.py user_10000-20000_community.txt –file output_distance_10000-20000.txt > output_closeness_centrality.txt

- Degree_centrality.py
	- Run in command line: python3 Degree_centrality.py -r dataproc --num-core-instances 4 data_10000-20000.txt –file user_10000-20000_community.txt > output_degree_centrality.txt
	
- Eigenvector_centrality.py
	- Run in command line: python3 Eigenvector_centrality.py user_10000-20000_community.txt –file data_10000-20000.txt > output_eigenvector_centrality.txt

 

## Problems
### 1. When setting the number of nodes to be 8, get errors: 
 - Insufficient 'DISKS_TOTAL_GB' quota. Requested 4500.0, available 4076.0.
 - Insufficient 'IN_USE_ADDRESSES' quota. Requested 9.0, available 8.0.">

### 2. CPU usage is around 6%. How to improve this?

### 3. When running on a larger file ~47 MB, 

- BrokenPipeError: [Errno 32] Broken pipe
: tried to output the file directly onto GCP

### 4. How to run on a 9.3 GB file? Split first or upload it onto GCP

### 5. Feasible to run in background?

### 6. Used a large amount of memory

## Usage
python3 FriendsRecommender.py -r dataproc --num-core-instances 12 ./data/friends-000______.txt --output-dir=gs://mrjob-us-central1-ab479002dcab930f/test_res/

python3 FriendsRecommender.py --jobconf mapreduce.job.reduces=1 ./data/friends-000______small.csv 


python3 FriendsRecommender.py -r dataproc --instance-type n1-highmem-2 --num-core-instances 30 gs://mrjob-us-central1-ab479002dcab930f/data/friends-000______.txt --output-dir=gs://mrjob-us-central1-ab479002dcab930f/test_res_000/

python3 FriendsRecommender.py -r dataproc --num-core-instances 3 gs://mrjob-us-central1-ab479002dcab930f/data/friends-000______small.txt > 000_small.txt

#### run_MRBFS.py
python run_MRBFS.py 902 222 
{the first number indicates the start node 
the second number indicates the end node}


