
import random
nodes = [i for i in range(1, 10)] # 0 has already been selected
r=2 # r=(1 +2*alpha) + r according to SODA paper  #Best for large dataset
while(len(nodes)):
    print(nodes)
    #k=random.randrange(r)
    k= random.choice(nodes[:r])
    nodes.remove(k)
    print(k)
    if(r<len(nodes)):
        r=2*r
    else:
        r=len(nodes)