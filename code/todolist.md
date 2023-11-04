1. read_data.py: need to check how you set the cost values
2. Note:
   - for your OD data, I add two columns: one stands for origin and the other is dest 
3. network.py: need to give edge different weight based on the type of the edge
4. formate the bus line data structure for the ND network

# Need to check and remark
1. the id index startng from 0
2. the link index starting from 1  ??
3. bus line index/id starting from 0
4. check how the types of different links are set
5. need to check the bus from node and to node index, whether they are the same as origin edges
6. append bus edges to net.edges, net.edges will be append to the graph of networkx. Then it will not affect using shortest path algorithm in the network graph packages

# Tasks: Deal with bus flow distribution and compute congestion 
- [x] create seperate python file
- [x] add bus class
- [x] read bus network data
- [x] compute bus travel time based on different bus frequnecy 
- [x] distribute flow to different bus lines 
- [x] compute bus congestion cost 


# Notes: steps to get the Bus network data
1. Run BTNDPV2 exe
2. if other network, need to create new network data set, and process data




# index