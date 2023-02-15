import sys
import math
import numpy as np
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

class Cube:
    def __init__(self, height, width, depth, shape):
        self.height = height
        self.width = width
        self.depth = depth
        self.shape = shape
        
    def mount_matrix(self, type_):
        arr = list(self.shape)
        if type_ == 'number':
            arr = [i for i in range(0,self.height*self.width*self.depth)]
            
        nn = []
        height = pit_height
        width = pit_width
        depth=pit_depth
        first = 0
        last = height*width
        for i in range(1,depth+1):
            nn.append(arr[first:last])
            first = last
            last = height*width*(i+1)

        n = []
        first = 0
        last = width
        for i in range(0,height):
            m=[]
            for j in range(0,depth):
                m.append(nn[j][first:last])
            n.append(list(np.array(m).flatten()))
            first = last
            last = first+width
        return n
    
    def get_min_max_height(self, char_shape):
        min_height = 0
        max_height = 0
        for i in range(1,len(char_shape)):
            indxs_ant = [i for i,x in enumerate(char_shape[i-1][0]) if x == '.']
            indxs_curr = [i for i,x in enumerate(char_shape[i][0]) if x == '.']
#             print(indxs_ant,indxs_curr)
            common_list = set(indxs_ant).intersection(indxs_curr)
            if len(common_list) == 0:
                min_height = i+1

            if len(common_list) > len(char_shape[0][0])/2:
                max_height=i-1
                break
#             print(i,common_list,len(p_shape[0][0])/2)

        return min_height, max_height

    def get_prohibted_indexes(self, obj):
        ind = set()
        for index, elem in enumerate(self.shape):
            if elem == obj:
                ind.add(index)
                if index > self.width * self.depth:
                    ind.add(index-self.width*self.depth)
        return ind
    
    
    def get_all_possibilities(self,n,pi,prohibited,height_index=0):
        layer = n[height_index]
        nnn = np.array(layer).reshape(self.depth,self.width)
        possibilities = []
        for ind,p in enumerate(pi):
    #         print("p",p)

            entry_shape = np.array(list(p[3]))
            entry_shape = entry_shape.reshape(p[2]*p[1],p[0])
    #         print(new_width)
            if p[1] >= 1:
                if p[1] <= self.width:
                    for i in range(self.depth-(p[1]-1)):
                        first = 0
                        last = self.width
    #                     print("i",i,nnn[i])
                        for j in range(self.width-(p[0]-1)):
                            el = nnn[i][first+j:p[0]+first+j]
    #                         print("j",el,entry_shape[0])

                            ell = [x for ind,x in enumerate(el) if entry_shape[0][ind] == '#']
    #                         print("j",el,entry_shape[0])
                            if any(x in prohibited for x in ell):
                                pass
                            else:
                                possibilities.append((el,p[4],j,i))
                        first=last
                        last = self.width+first
            if p[1] > 1:
                if p[1] <= self.depth:
                    nnn = np.rot90(nnn)
                    for i in range(self.depth-(p[0]-1)):
                        first = 0
                        last = self.width
    #                     print("ii",i,nnn[i])
                        for j in range(self.width-(p[1]-1)):
                            el = nnn[i][first+j:p[1]+first+j]
                            # print(el,first+j,p[1]+first+j)
                            if any(x in prohibited for x in el):
                                pass
                            else:
                                possibilities.append((el,p[4],j,i))
                        first=last
                        last = self.width+first

        return possibilities

    def check_bad_good_possibility(self,x,entry,entry_shape,arr_shape,height_index):
        for i in range(entry[2]):
            for j in range(entry[0]):
    #             print(i+height_index,j+x)
                if self.depth > 1:
                    return True
                else:
                    if arr_shape[i+height_index][j+x] != '#':
                        arr_shape[i+height_index][j+x] = entry_shape[i][j]
                    elif arr_shape[i+height_index][j+x] == '#' and entry_shape[i][j] == '#':
    #                     print("aqui1")
                        return False
                    if i+height_index > height_index:
                        if entry_shape[i][j] == '#':
                            if arr_shape[i+height_index-1][j+x] == '.':
    #                             print("aqui2")
                                return False

        return True
    
    def get_improved_possibilities(self,possibilities):
        good_possibilities = []
        bad_possibilities = []
        for p in possibilities:
    #         p = possibilities[1]
            arr_shape=np.array(self.mount_matrix('char'))
        
            a, pind, x, z = p
    #         print(p)
            entry = [x for x in pi if int(x[4]) == pind][0]
            entry_shape = np.array(list(entry[3]))
            entry_shape = entry_shape.reshape(entry[2]*entry[1],entry[0])
            good = self.check_bad_good_possibility(x,entry, entry_shape,arr_shape,height_index)
            if good:
                good_possibilities.append((a, pind, x, z))
            else:
                bad_possibilities.append((a, pind, x, z))
        return good_possibilities, bad_possibilities

# game loop
count_high_index = 0
height_index=0
last_count_row = 0
while True:
    inputs = input().split()
    pit_width = int(inputs[0])
    pit_height = int(inputs[1])
    pit_depth = int(inputs[2])
    pit_shape = inputs[3]
    
    cube = Cube(pit_height,pit_width,pit_depth,pit_shape)

    print(inputs,file=sys.stderr, flush=True)
    n = cube.mount_matrix('number')
    p_shape = cube.mount_matrix('char')
    
    block_count = int(input())
    print(block_count, file=sys.stderr, flush=True)
    pi = []
    for i in range(block_count):
        inputs = input().split()
        block_index = int(inputs[0])
        width = int(inputs[1])
        height = int(inputs[2])
        depth = int(inputs[3])
        shape = inputs[4]
        if int(depth) <= int(pit_depth): 
            pi.append((width, depth,height, shape,block_index))
            print(inputs, file=sys.stderr, flush=True)
   
    # pi = [p for p in pi if p[0] <= pit_width and p[1] <= pit_depth]

    prohibited = cube.get_prohibted_indexes("#")
    # print("get prohibted", prohibited, file=sys.stderr, flush=True)
    # print("pi", pi, file=sys.stderr, flush=True)
    
    good_possibilities = [] 
    bad_possibilities = []
    min_height = 0
    max_height= len(p_shape)
    # print(n,file=sys.stderr, flush=True)
    for i in range(1,len(p_shape)):
        indxs_ant = [i for i,x in enumerate(p_shape[i-1]) if x == '.']
        indxs_curr = [i for i,x in enumerate(p_shape[i]) if x == '.']
        common_list = set(indxs_ant).intersection(indxs_curr)
        if len(common_list) == 0:
            min_height = i+1
        
        if len(common_list) > len(p_shape[0])/2 and i > 1:
            max_height=i
            break
    # print(min_height,max_height,file=sys.stderr, flush=True)
    height_index_list = [i for i in range(min_height,max_height)]
    # print("height_index_list",height_index_list,file=sys.stderr, flush=True)
    for hi in height_index_list:
        # print("hi", hi, file=sys.stderr, flush=True)
        possibilities = cube.get_all_possibilities(n,pi,prohibited,hi)
        if len(possibilities) == 0:
            continue

        # print("height_index",hi,file=sys.stderr, flush=True)
        # print("possibilities",pit_depth,possibilities, file=sys.stderr, flush=True)

        # good_possibilities, bad_possibilities = get_improved_possibilities(possibilities,pit_shape,pit_height,pit_width,pit_depth)
        good_possibilities, bad_possibilities = cube.get_improved_possibilities(possibilities)
        if len(good_possibilities) > 0:
            break
        else:
            continue

    # print("good",good_possibilities, file=sys.stderr, flush=True)
    # print("bad",bad_possibilities, file=sys.stderr, flush=True)

    if len(good_possibilities) > 0:
        print(good_possibilities[0][1], good_possibilities[0][2], good_possibilities[0][3])
    else:
        print(bad_possibilities[0][1], bad_possibilities[0][2], bad_possibilities[0][3])

    count_high_index += 1


