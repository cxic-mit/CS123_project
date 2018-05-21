# CMSC 12300: Computer Science with Applications III Project
Team Members: Xi Chen, Yangyang Dai, Rose Gao, Liqiang Yu

Files:
1. Exploration.ipynb: initial exploration of Friendster dataset
2. FriendsRecommender.py
	- Run in command line: python3 FriendsRecommender.py --jobconf mapreduce.job.reduces=1 data/small.txt > data/output.txt
3. data (contains a short sample text file)
4. Proposal (contains our initial proposed project)

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

~70 GB
killed 9


python3 FriendsRecommender.py -r dataproc --num-core-instances 12 ./data/friends-000______.txt --output-dir=gs://mrjob-us-central1-ab479002dcab930f/test_res/

python3 FriendsRecommender.py --jobconf mapreduce.job.reduces=1 ./data/friends-000______small.csv 

python3 FriendsRecommender.py -r dataproc --instance-type n1-highmem-2 --num-core-instances 30 gs://mrjob-us-central1-ab479002dcab930f/data/friends-000______.txt --output-dir=gs://mrjob-us-central1-ab479002dcab930f/test_res_000/



### To do

Learn to use screen to run mrjob in 'background'.

Imporve the performance of FriendRecommender.py



