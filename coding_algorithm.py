import sys
import numpy as np

class Cube:
    def __init__(self, height, width, depth, shape):
        self.height = height
        self.width = width
        self.depth = depth
        self.shape = shape
        
    def mount_matrix(self, type_):
        """
        Returns a 2d matrix from the original shape.
        If type_ is 'number', the elemens will consistis in a index matrix. 
        Ex: [[0, 1, 2, 24, 25, 26, 48, 49, 50],
            [3, 4, 5, 27, 28, 29, 51, 52, 53],
            [6, 7, 8, 30, 31, 32, 54, 55, 56],
            [9, 10, 11, 33, 34, 35, 57, 58, 59],
            [12, 13, 14, 36, 37, 38, 60, 61, 62],
            [15, 16, 17, 39, 40, 41, 63, 64, 65],
            [18, 19, 20, 42, 43, 44, 66, 67, 68],
            [21, 22, 23, 45, 46, 47, 69, 70, 71]]
        If type_ is 'char', the elements will consistis in a character matrix. 
        Ex: [['#', '#', '#', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.']]

        :param type_: string

        :return list:
        """
        arr = list(self.shape)
        if type_ == 'number':
            arr = [i for i in range(0,self.height*self.width*self.depth)]
            
        arr_row = []
        height = pit_height
        width = pit_width
        depth=pit_depth
        first = 0
        last = height*width
        for i in range(1,depth+1):
            arr_row.append(arr[first:last])
            first = last
            last = height*width*(i+1)

        arr_final = []
        first = 0
        last = width
        for i in range(0,height):
            m=[]
            for j in range(0,depth):
                m.append(arr_row[j][first:last])
            arr_final.append(list(np.array(m).flatten()))
            first = last
            last = first+width
        return arr_final
    
    def get_min_max_height(self, char_shape):
        """
        Returns the layer hight which the algorithm will try to fit the current block.
        Ex: In a clube with shape (3,8,4), 3 is the width, 8 is the height and 4 is the depth.
            As the height is 8, than the cube has 8 layers.

        :param char_shape: list [string]

        :return int:
        """
        min_height = 0
        max_height = 0
        for i in range(1,len(char_shape)):
            indxs_ant = [i for i,x in enumerate(char_shape[i-1][0]) if x == '.']
            indxs_curr = [i for i,x in enumerate(char_shape[i][0]) if x == '.']
            common_list = set(indxs_ant).intersection(indxs_curr)
            if len(common_list) == 0:
                min_height = i+1

            if len(common_list) > len(char_shape[0][0])/2:
                max_height=i-1
                break

        return min_height, max_height

    def get_prohibted_indexes(self, obj):
        """
        Returns the the indexes that are already filled.
        
        :param obj: string (we use the char '#' to make reference to the filled spaces inside of the cube)

        :return set (int):
        """
        ind = set()
        for index, elem in enumerate(self.shape):
            if elem == obj:
                ind.add(index)
                if index > self.width * self.depth:
                    ind.add(index-self.width*self.depth)
        return ind
    
    
    def get_all_possibilities(self,number_shape,pi,prohibited,height_index=0):
        """
        Returns all possibilities to fit the block inside the current state of the cube.
        
        :param number_shape: list[int]
        :param pi: list[ tuple ]
        :param prohibited: list[ int ]
        :param height_index: int

        :return list [int]:
        """
        layer = number_shape[height_index]
        nnn = np.array(layer).reshape(self.depth,self.width)
        possibilities = []
        for ind,p in enumerate(pi):
            entry_shape = np.array(list(p[3]))
            entry_shape = entry_shape.reshape(p[2]*p[1],p[0])
            if p[1] >= 1:
                if p[1] <= self.width:
                    for i in range(self.depth-(p[1]-1)):
                        first = 0
                        last = self.width
                        for j in range(self.width-(p[0]-1)):
                            el = nnn[i][first+j:p[0]+first+j]
                            ell = [x for ind,x in enumerate(el) if entry_shape[0][ind] == '#']
                            if any(x in prohibited for x in ell):
                                # TODO create a mothod to convert the block to 2d matrix and check possibilities
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
                        for j in range(self.width-(p[1]-1)):
                            el = nnn[i][first+j:p[1]+first+j]
                            if any(x in prohibited for x in el):
                                # TODO create a mothod to convert the block to 2d matrix and check possibilities
                                pass
                            else:
                                possibilities.append((el,p[4],j,i))
                        first=last
                        last = self.width+first

        return possibilities

    def check_bad_good_possibility(self,x,entry,entry_shape,arr_shape,height_index):
        """
        Check if current block satifies the condition to be classified as a good or bad possibility
        
        :param entry: list[ tuple ]
        :param entry_shape: list[ string ]
        :param arr_shape: list[ string ]
        :param height_index: int

        :return boolean:
        """
        for i in range(entry[2]):
            for j in range(entry[0]):
                if self.depth > 1:
                    return True
                else:
                    if arr_shape[i+height_index][j+x] != '#':
                        arr_shape[i+height_index][j+x] = entry_shape[i][j]
                    elif arr_shape[i+height_index][j+x] == '#' and entry_shape[i][j] == '#':
                        return False
                    if i+height_index > height_index:
                        if entry_shape[i][j] == '#':
                            if arr_shape[i+height_index-1][j+x] == '.':
                                return False

        return True
    
    def get_improved_possibilities(self,possibilities):
        """
        Split all the possibilities into a set of good or bad possibilities
        
        :param entry: possibilities[ int ]

        :return list [int], list [int]:
        """
        good_possibilities = []
        bad_possibilities = []
        for p in possibilities:
            arr_shape=np.array(self.mount_matrix('char'))
        
            a, pind, x, z = p

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

    number_shape = cube.mount_matrix('number')
    char_shape = cube.mount_matrix('char')
    
    block_count = int(input())
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

    prohibited = cube.get_prohibted_indexes("#")

    min_height = 0
    max_height= len(char_shape)
    # define which layers will the checked
    for i in range(1,len(char_shape)):
        indxs_ant = [i for i,x in enumerate(char_shape[i-1]) if x == '.']
        indxs_curr = [i for i,x in enumerate(char_shape[i]) if x == '.']
        common_list = set(indxs_ant).intersection(indxs_curr)
        if len(common_list) == 0:
            min_height = i+1
        
        if len(common_list) > len(char_shape[0])/2 and i > 1:
            max_height=i
            break
    
    good_possibilities = [] 
    bad_possibilities = []
    height_index_list = [i for i in range(min_height,max_height)]

    # find good possibilities in all layers of the cube
    for hi in height_index_list:
        possibilities = cube.get_all_possibilities(number_shape,pi,prohibited,hi)
        if len(possibilities) == 0:
            continue

        good_possibilities, bad_possibilities = cube.get_improved_possibilities(possibilities)
        if len(good_possibilities) > 0:
            break
        else:
            continue

    if len(good_possibilities) > 0:
        # TODO create a method to select the better option inside good possibilities
        print(good_possibilities[0][1], good_possibilities[0][2], good_possibilities[0][3])
    else:
        # TODO create a method to select the better option inside bad possibilities
        print(bad_possibilities[0][1], bad_possibilities[0][2], bad_possibilities[0][3])

    count_high_index += 1


