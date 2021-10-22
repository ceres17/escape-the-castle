# recursive backtracking | 19/09/21

import random, time

def generateTree(maxX, maxY):

    nodes = []

    for x in range(1,maxX+1):
        for y in range(1,maxY+1):
            nodes.append((x, y))

    adjacent_nodes = ((-1, 0), (1,0), (0,1), (0, -1))

    stack = []
    spanning_tree = []

    start_time = time.time()

    next_node = (1,1)

    while True:

        current_node = next_node
        stack.append(current_node)

        try:
            nodes.remove(current_node)
        except ValueError:
            pass

        possible_nodes = []

        # finding possible next nodes by comparing each position adjacent to the current node to the unused nodes
        for dx, dy in adjacent_nodes:
            if (current_node[0] + dx, current_node[1] + dy) in nodes:
                possible_nodes.append((current_node[0] + dx, current_node[1] + dy))
        if possible_nodes:
            # choosing a random (adjacent) node to go next
            next_node = random.choice(possible_nodes)
            spanning_tree.append((next_node, current_node))
        else:
            # checking each node from the stack for possible nodes, if there are none, removing it
            for index in range(len(stack)-1, -1, -1):
                check_node = stack[index]
                for dx, dy in adjacent_nodes:
                    if (check_node[0] + dx, check_node[1] + dy) in nodes:
                        next_node = check_node; break
                else:
                    try:
                        stack.remove(check_node) # using stack to keep track of which nodes to/ not to visit again
                    except ValueError:
                        pass
                    continue
                break
        
        if len(stack) == 0:
            break

    end_time = time.time()-start_time
    print((str(end_time)[:-(len(str(end_time).split('.')[1])-2)]) + 's')
    return spanning_tree

'''
file = open('spanning-tree.txt', 'a')
file.truncate(0) # empties the file before writing new tree
for item in spanning_tree:
    #            {      coordinate going to        } {       coordinate coming from    }
    file.write(f'{str(item[0][0])},{str(item[0][1])},{str(item[1][0])},{str(item[1][1])}\n')
    '''