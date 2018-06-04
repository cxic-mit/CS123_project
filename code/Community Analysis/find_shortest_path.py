#Given a node, this function finds shortest path to another node a
#This function can be used to find the shortest path after MRBFS and run_MRBFS file. 

def find_shortest_path(a):
    for i in data:
        l=i.split("|")

        if l[0]==str(a):
            shortest_path=l[-2]
            return shortest_path