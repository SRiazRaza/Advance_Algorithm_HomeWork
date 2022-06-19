with open("mst_dataset\input_random_04_10.txt", "r") as file:
    graphInfo = file.readline().split(" ")
    #print(graphInfo)
    # Storing graph info
    noOfVertices = int(graphInfo[0])
    noOfEdges = int(graphInfo[1])
    #print(noOfVertices,noOfEdges)

    # Adding edges to the graph

    
    lines = file.readlines()
    # Adding edges to the graph
    for x in lines:
        x=x.strip()
        x=x.split(" ")
        print(int(x[0]),int(x[1]),int(x[2]))
