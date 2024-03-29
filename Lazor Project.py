'''
Lazor project
author: Ruihao Ni, Huaizhong Zhang

1. arrange A B C into the empty O site to generate 
a random distribution of the box.

2. Convert the box into the point with transmission/reflection 
condition with the coordnation.

3. put the laser ray in and generate all the point which the 
ray pass through.

4. Check that if all the expected point have a ray come through.
Type of variate: list of list

1. Box: 
   box[]

    (1) Center position (cx, cy): 
        (1,1) (3,1) (5,1) (7,1)
        (1,3) (3,3) (5,3) (7,3)

    (2) Box type: box_type: A/ B/ C/ o/ x
    x = no block allowed
    o = blocks allowed
    A = fixed reflect block
    B = fixed opaque block
    C = fixed refract block

    [(cx, cy), boxtype]

2. Grid Point:

    grid_point[]

    (1) Position: (gx, gy)

    (2) orientation (ox, oy): 
    up (0, -1) / down (0,1) / left (-1, 0) / right (1, 0)

    (3) type: o/ A/ B/ C
    o: pass the point
    A: reflect
    B: terminate the ray
    C: pass and reflect

3. Ray point:

    a for loop
    1. put the original input point in the in_rpoint[]


    incident ray point:
    in_rpoint[]

    (1) position (irx, iry)
    (2) direction(vx, vy) 

    [[irx, iry], [vx, vy] 
    (same format as the given input laser)

    2. save the position of the input point in a list

    passpoint [(gx,gy)] 


    3. find all of the output point out_rpoint

    out_rpoint[]
    [[orx, ory], [vx, vy]
    convert to next incident ray point

    next in_rpoint[]:
    irx = orx + vx
    iry = ory + vy

    4. convert to next incident point in_rpoint[]
    then start overt

'''
import itertools
from copy import deepcopy
from PIL import Image

def read_bff(filename, select):
    '''
    finished by Ruihao

    Read the bff file and pick up all the information

    **Parameters**
    filename: *str*
    The .bff file that contains all the Lazor information

    select: *str*
    the selector to choose which value will be returned

    **Return**
    box_raw: *list*
    [[o, o, o],
    [o, A, x],
    [B, o, x]]

    box: *list*
    box with coordination

    size of the box
    w, h: *tuple*
    how many boxes per line/column

    number of A, B, C: *tuple*
    nA, nB, nC

    start point: *list*
    [[rx, ry], [vx, vy)] 

    end point: *list*
    [x,y]
    '''
    fi = open(filename, 'r')
    bff = fi.read()
    line_split = bff.strip().split('\n')

    box_raw = []
    box = []
    start_point = []
    end_point = []
    a = line_split.index('GRID START')
    b = line_split.index('GRID STOP')

    for line in line_split[a+1:b]:

        box_line = []
        for i in line:
            if i != ' ':
                box_line.append(i)
        box_raw.append(box_line)
# convert box raw to box with [(cx,cy), boxtype]

    for y in range(len(box_raw)):
        for x in range(len(box_raw[y])):
            box.append([[2 * x + 1, 2 * y + 1], box_raw[y][x]])
# convert the start point, end point and number of boxes into lists
    nA, nB, nC = 0, 0, 0
    for line in line_split[b+1:(len(line_split))]:
        if line.startswith('A'):
            nA = int(line[2])
        elif line.startswith('B'):
            nB = int(line[2])
        elif line.startswith('C'):
            nC = int(line[2])
        elif line.startswith('L'):
            s_p = line.strip().split(' ')

            start_point.append([[int(s_p[1]), int(s_p[2])], [(int(s_p[3])), int(s_p[4])]])

        elif line.startswith('P'):
            end_point.append([int(line[2]), int(line[4])])

    w = len(box_raw[0])
    h = len(box_raw)

    # the command which been commented out are used for testing
    # print('box_raw')
    # print(box_raw)
    # print('w,h')
    # print(w,h)
    # print('box')
    # print(box)
    # print('nA, nB, nC')
    # print(nA, nB, nC)
    # print('start_point')
    # print(start_point)
    # print('end_point')
    # print(end_point)

    if select == 'br':
        return box_raw
    elif select == 'size':
        return w, h  
    elif select == 'box':
        return box
    elif select == 'nABC':
        return nA, nB, nC
    elif select == 'sp':
        return start_point
    elif select == 'ep':
        return end_point

    fi.close()

def convert_box(box):
    '''
    finished by Ruihao

    **Parameters**
    box: *list*
    a list of the original box
    [[cx,cy], gridtype]

    **Returns**
    grid point:*list*
    [[gx, gy], [ox, oy], gridtype]

    convert the box to grid point with the type
    (orientation (ox, oy):
    up (0, -1) / down (0,1) / left (-1, 0) / right (1, 0)
    (3) type: o/ A/ B/ C
    o: pass the point
    A: reflect
    B: terminate the ray
    C: pass and reflect
    '''
    grid_point = []

    for b in box:
        x, y = b[0]
        gridtype = b[1]
        u = [[x, y-1], [0, -1], gridtype]
        d = [[x, y+1], [0, 1], gridtype]
        l = [[x-1, y], [-1, 0], gridtype]
        r = [[x+1, y], [1, 0], gridtype]
        grid_point.append(u)
        grid_point.append(l)
        grid_point.append(d)
        grid_point.append(r)

    return grid_point

def convert_grid(grid):
    '''
    finished by Ruihao

    **Parameters**
    grid point:*list*
    [[gx, gy], [ox, oy], gridtype]
    
    **Returns**
    box: *list*
    a list of the original box
    [[cx,cy], gridtype]
    
    convert the box to grid point with the type
    (orientation (ox, oy):
    up (0, -1) / down (0,1) / left (-1, 0) / right (1, 0)
    (3) type: o/ A/ B/ C
    o: pass the point
    A: reflect
    B: terminate the ray
    C: pass and reflect
'''
    if grid[1] == [-1, 0]:
        return [[grid[0][0] + 1, grid[0][1]], grid[2]]
    if grid[1] == [1, 0]:
        return [[grid[0][0] - 1, grid[0][1]], grid[2]]
    if grid[1] == [0, -1]:
        return [[grid[0][0], grid[0][1] + 1], grid[2]]
    if grid[1] == [0, 1]:
        return [[grid[0][0], grid[0][1] - 1], grid[2]]

# given a incident ray, find the grid point that face to the ray (can reflect)

def find_gp1(filename, point):
    '''
    finished by Ruihao

    **Parameters**
    filename: *str*
    The .bff file that contains all the Lazor information
   
    ray point: *list*
    [[cx,cy],[vx, vy]]
    position, direcction

    **Returns**
    grid point:*list*
    [[gx, gy], [ox, oy], gridtype]
    position, direction, type
    
    for a ray point, find the grid point(side of box)
    that face the ray(can reflect the ray)
    '''
    w, h = read_bff(filename, 'size')
    gp = (0, 0, 0)

    if point[0][0] >= 0 and point[0][0] <= 2*w and point[0][1] >= 0 and point[0][1] <= 2*h:
        grid = convert_box(read_bff(filename, 'box'))
        if point[0][0] % 2 == 0:
            face = [-point[1][0], 0]
        if point[0][0] % 2 != 0:
            face = [0, -point[1][1]]
        for i in range(len(grid)):
            if grid[i][0] == point[0] and grid[i][1] == face:
                gp = grid[i]
                break
        return gp
    else:
        return 'out'

def first_line(filename, n):
    '''
    Finished by Ruihao

    **Parameters**
    filename: *str*
    The .bff file that contains all the Lazor information

    n: *int*
    select which of the ray
    generate line for n line
    
    use the initial condition to find the boxes on the line

    '''

    start_point = read_bff(filename, 'sp')
    pline = start_point[n-1]
    # print (pline)
    # print(find_gp1(filename, pline))
    path = []
    # for i in range(4):
    while find_gp1(filename, pline) != 'out':
        gp_line = find_gp1(filename, pline)
        if gp_line[2] == 'o':
            path.append(gp_line)
        pline[0][0] = pline[0][0] + pline[1][0]
        pline[0][1] = pline[0][1] + pline[1][1]
    blockpath = []
    for i in path:
        blockpath.append(convert_grid(i))
    return blockpath

class Block():
    '''
    Finished by Huaizhong Zhang

    This class object describes different types of blocks in the game
    and how do they affect the laser touching them
    'o' or 'x' are no blocks
    'A' is a reflect block
    'B' is a opaque block
    'C' is a refract block        
    '''
    
    def __init__(self, grid_point, l_start_point): 
        '''
        initializing the block
        **Parameters**
            grid_point: *list, int, str*
                a list of int and str contains the position 
                and type of a grid_point
            l_start_point: *list, int*
                a list of int contains the position and 
                direction of the laser before touching a block
        **Returns**
            new_l1: *list, int*
                a list of int contains the position and 
                direction of the laser after touching a block
            new_l2: *list, int*
                a list of int contains the position and 
                direction of the laser after touching a block               
        '''
        self.grid_point = grid_point
        self.l_start_point = l_start_point
        self.new_l1 = []
        self.new_l2 = []
    
        if self.grid_point[2] == 'o' or 'x':
            self.new_l1 = self.l_start_point
        if self.grid_point[2] == 'A':
            self.new_l1 = self.reflect()
        if self.grid_point[2] == 'B':
            self.new_l1 = self.opaque()
        if self.grid_point[2]== 'C':
            self.new_l1, self.new_l2 = self.refract()
           
    def reflect(self):
        '''
        accounting for the affect of block 'A' to the laser        
        '''
        if self.grid_point[1][0] == 0:
            self.l_start_point[1][1] = -self.l_start_point[1][1]
            self.new_l1 = self.l_start_point
        if self.grid_point[1][0] != 0:
            self.l_start_point[1][0] = -self.l_start_point[1][0]
            self.new_l1 = self.l_start_point
        return self.new_l1
                    
    def refract(self):
        '''
        accounting for the affect of block 'C' to the laser        
        '''
        self.new_l2 = deepcopy(self.l_start_point)
        self.reflect()
        return self.new_l1, self.new_l2
        
    def opaque(self):
        '''
        accounting for the affect of block 'B' to the laser        
        '''
        self.l_start_point[1][0] = 0
        self.l_start_point[1][1] = 0
        self.new_l1 = self.l_start_point
        return self.new_l1     
    
def find_gp(grid, point, filename):
    '''
    find the desire grid point for a given laser starting point
    **Parameters**
        grid:*list, int, str*
            a list of int and str contains the position and 
            type of a list of grid points
        point:*list, int*
            a list of int contains the position and direction
            of a given laser starting point
        filename:*str*
            a string contains the name of the game we want to solve
    **Returns**
        gp:*list, int, str*
            a lsit of int and str contains the position and type 
            of the desire grid point
    '''
    w, h = read_bff(filename, 'size')
    gp = []
    # if the laser starting point is in the boundary
    if point[0][0] > 0 and point[0][0] < 2*w and point[0][1] > 0 and point[0][1] < 2*h:
        if point[0][0] % 2 == 0:
            face = [-point[1][0], 0]
        if point[0][0] % 2 != 0:
            face = [0, -point[1][1]]
        for i in range(len(grid)):
            if grid[i][0] == point[0] and grid[i][1] == face:
                gp = grid[i]
                break
        return gp   
    # if the laser starting point is on the boundary
    # but the direction is inside the boundary
    if point[0][0] == 0 and point[1][0] == 1: 
        face = [-point[1][0], 0]
        for i in range(len(grid)):
            if grid[i][0] == point[0] and grid[i][1] == face:
                gp = grid[i]
                break
        return gp
    
    if point[0][0] == 2*w and point[1][0] == -1:
        face = [-point[1][0], 0]
        for j in range(len(grid)):
            if grid[j][0] == point[0] and grid[j][1] == face:
                gp = grid[j]
                break
        return gp 
      
    if point[0][1] == 0 and point[1][1] == 1:
        face = [0, -point[1][1]]
        for k in range(len(grid)):
            if grid[k][0] == point[0] and grid[k][1] == face:
                gp = grid[k]
                break
        return gp
    
    if point[0][1] == 2*h and point[1][1] == -1:
        face = [0, -point[1][1]]
        for l in range(len(grid)):
            if grid[l][0] == point[0] and grid[l][1] == face:
                gp = grid[l]
                break      
        return gp
    # if the laser starting point is on the boundary
    # and the direction is outside the boundary            
    if point[0][0] == 0 and point[1][0] == -1: 
        gp = [[],[],'B']
        return gp
    
    if point[0][0] == 2*w and point[1][0] == 1:
        gp = [[],[],'B']
        return gp   
     
    if point[0][1] == 0 and point[1][1] == -1:
        gp = [[],[],'B']
        return gp  
    
    if point[0][1] == 2*h and point[1][1] == 1:
        gp = [[],[],'B']
        return gp
    # if the laser starting point is out of the boundary
    if point[0][0] < 0 or point[0][0] > 2*w or point[0][1] < 0 or point[0][1] > 2*h:
        gp = [[],[],'B']
        return gp   

    raise Exception("Error - Something went wrong here")
        
def update_laser(grid_points, l_start_points, filename):
    '''
    updating the position and direction of given 
    laser starting points after it touching the next block    
    **Parameters**
        grid_points:*list, int, str*
            a list of int and str contains the position and 
            type of a list of grid points
        l_start_points:*list, int*
            a list of int contains the position and direction
            of given laser starting points
        filename:*str*
            a string contains the name of the game we want to solve
    **Returns**
        laser_out_points:*list, int*
            a lsit of int contains the position and direction
            of of given laser starting points after it touching the next block
    '''
    laser_out_points = []
    
    for i in range(len(l_start_points)):
        grid_point = find_gp(grid_points, l_start_points[i], filename)
        a = Block(grid_point, l_start_points[i])
        new_l1 = a.new_l1
        new_l2 = a.new_l2
        if len(new_l1) != 0 and new_l1[1][0] != 0:
            new_l1[0][0] = new_l1[0][0] + new_l1[1][0]
            new_l1[0][1] = new_l1[0][1] + new_l1[1][1]            
            laser_out_points.append(new_l1)
                
        if len(new_l2) != 0 and new_l2[1][0] != 0:
            new_l2[0][0] = new_l2[0][0] + new_l2[1][0]
            new_l2[0][1] = new_l2[0][1] + new_l2[1][1]
            laser_out_points.append(new_l2)
            
    return(laser_out_points)
    
def test_solution(grid_points, l_start_points, end_points, filename):
    '''
    testing whether the given grid points could sovle the laser game 
    **Parameters**
        grid_points:*list, int, str*
            a list of int and str contains the position and 
            type of a list of grid points
        l_start_points:*list, int*
            a list of int contains the position and direction
            of given laser starting points
        end_points:*list, int*
            a list of int contains the position of the target points        
        filename:*str*
            a string contains the name of the game we want to solve
    **Returns**
        True:
            the game has been sovled
        False:
            the game has not been solved
    '''
    laser_path_point = []
    laser_path_point1 = []
    same_xy = 0
    laser_path_point2 = []

    while len(l_start_points) > 0:
        laser_path_point = laser_path_point + deepcopy(l_start_points)
        l_start_points = update_laser(grid_points, l_start_points, filename)
    
    for i in range(len(laser_path_point)):
        laser_path_point1 = laser_path_point1 + [laser_path_point[i][0]]
    
    for item in laser_path_point1:
        if not item in laser_path_point2:
            laser_path_point2.append(item)
        
    for j in range(len(end_points)):
        for k in range(len(laser_path_point2)):
            if end_points[j] == laser_path_point2[k]:
                same_xy = same_xy + 1

    if len(end_points) == same_xy:
        return True
    if len(end_points) != same_xy:
        return False
    
def set_colors(img, x0, y0, dim, gap, color):
    for x in range(dim):
        for y in range(dim):
            img.putpixel((gap + (gap+dim)*x0 + x, gap + (gap+dim)*y0 + y),
                         color
                    )            

def solution_output(solution0,filename, dim=50, gap=5):
    '''
    Converting the output of the answer to an image
    **Parameters**
        Solution0:*list, int, str*
            a list of int and str contains output (the position and 
            type of a list of grid points)       
        filename:*str*
            a string contains the name of the game we want to solve
    **Returns**
        None
    '''    
    w, h = read_bff(filename, 'size')
    colors ={'o':(192, 192, 192),
         'x':(128, 128, 128),
         'A':(203, 228, 255),
         'B':(0,0,0),
         'C':(245,245,245),
         'gap':(128, 128, 128)
        }
    solution1  = []
    solution2 = []
    x = 0
    for j in range(int(len(solution0)/w)):
        for i in range(int(len(solution0)/h)):
            solution1.append(solution0[w*x + i][1])
        solution2.append(solution1)
        x = x + 1
        solution1 = []
    
    w_blocks = len(solution2[0])
    h_blocks = len(solution2)
    size = (w_blocks*(dim+gap) + gap, h_blocks*(dim+gap) + gap)
    img = Image.new("RGB", size, color=colors['gap'])

    
    for y1, y2 in enumerate(solution2):
        for x1, x2 in enumerate(y2):
            set_colors(img, x1, y1, dim, gap, colors[x2])
            
    img.show()
            
    img.save('Solution.png')

def solve(filename):
    '''
    Finished by Ruihao

    **Parameters**
    filename: *str*
    The .bff file that contains all the Lazor information

    some trial on brute force to solve the maze is found to be impossible when
    the overall block exceed 12, so we need some strategy when we try to put
    ABC block on the availabe position on o.
    the order of assigning the position: refract and reflect box (refl),
    then the opaque boxes
    '''

    import_box = read_bff(filename, 'box')
    nA, nB, nC = read_bff(filename, 'nABC')
    # print(nA, nB, nC)
    obox = []
    for i in import_box:
        if i[1] == 'o':
            obox.append(i)

    Al, Bl, Cl = [], [], []

    if nA:
        Al = ['A'] * nA
    if nB:
        Bl = ['B'] * nB
    if nC:
        Cl = ['C'] * nC
    #  Al: AAAAA Bl: BBBBB    
    rbox_raw = Al + Cl
    solved = False

    if nA + nC == 0:
        solved = True
        # print('dark')        
        # directly pass e.g. dark_1.bff
        boxop_left = obox
        grid_s1 = import_box
        box_left = Bl

        # save the following variables:
        # rest block yet to be put in
        # obox rest ()
        # solved grid(initial grid)

    else:
        rbox_tuple = list(set(itertools.permutations(''.join(rbox_raw))))
        refl = []
        for i in rbox_tuple:
            refl.append(list(i))
        # print('refl')
        # print(refl) # refl: permutation of all the reflect/refract box
        # [['A', 'A', 'C'], ['A', 'C', 'A']]
        # print(obox)
        line1 = first_line(filename, 1)
        # print(line1)
        # if len(read_bff(filename, 'sp')) == 1 or len(read_bff(filename, 'sp')) == 2:
        # for very big box with two or more incident light, we can use two for loop to 
        # accelerate the calculation.
        if solved is False:
            for f1 in line1:  # select a box in the first line
                if solved is True:
                    break
                # print('f1')
                # print(f1)
                # [[1,3],'o']
                for br in refl:  # select an order of A C arrangement
                    # select on and put in(save the box)

                    # update refl (delete the box which put inside)
                    # change the box
                    # combination
                    grid_1 = deepcopy(import_box)
                    if solved is True:
                        break

                    # this part use a for loop to find the same box, can be upgraded
                    for i in range(len(grid_1)):
                        if grid_1[i][0] == f1[0]:
                            grid_1[i][1] = br[0]
                            break
                    boxoption = deepcopy(obox)
                    boxoption.remove(f1)
                    # after put first box, the rest available box
                    boxoption = list(itertools.combinations(boxoption, len(br)-1))
                    # print('grid_1')
                    # print(grid_1)
                    # print('boxoption')
                    # print(boxoption)
                    # put the other boxes in
                    for box_op in range(len(boxoption)): # select an order of combination
                        if solved is True:
                            break
                        usedbox = [br[0]]
                        grid_2 = deepcopy(grid_1)  # copy the grid with the first box put in
                        # record the used box
                        # update the grid
                        # print the grid
                        for box1 in range(len(br)-1):
                            # print('br =', br)
                            # print('boxoption[box_op]')
                            # print(boxoption[box_op])
                            for i in range(len(grid_2)):
                                # print(1, grid_2[i][0])
                                # print(2, boxoption[box_op][box1])
                                if grid_2[i][0] == boxoption[box_op][box1][0]:
                                    grid_2[i][1] = br[box1+1]
                                    break
                            usedbox.append(br[box1+1])
                            # print('used box')
                            # print(usedbox)
                            # print('grid_2')
                            # print(grid_2)
                            l_start_points = read_bff(filename, 'sp')
                            end_points = read_bff(filename, 'ep')
                            gridpoints_2 = convert_box(grid_2)  #convert box to grid point

                            if (test_solution(gridpoints_2, l_start_points, end_points, filename)):
                                solved = True
                                # print(grid_2)

                                boxop_left = [box3 for box3 in grid_2 if box3[1] == 'o']

                                brleft = deepcopy(list(br))
                                # print(brleft)
                                for i in usedbox:
                                    brleft.remove(i)
                                # print(brleft)
                                box_left = Bl + brleft
                                # print(box_left)
                                grid_s1 = grid_2

                                break
                                # update the grid 
                                # check whether all the point demanded have light passed through
                                # record the grid
        # the following code can be used if there are two or
        # more incident light and the box is big.
        # elif len(read_bff(filename, 'sp')) == 2:
        #     line2 = first_line(filename, 2)
        #     if solved == False:#while
        #         for br in refl:
        #             if solved == True:
        #                 break
        #                 # select an order of A C arrangement
        #                 # select on and put in(save the box)
        #             for f1 in line1: # select a box in the first line
        #                 if solved == True:
        #                     break
        #                 # print('f1')
        #                 # print(f1)
        #                 # [[1,3],'o']
        #                 # change the box
        #                 # combination
        #                 grid_x = deepcopy(import_box)
        #                 # this part use a for loop to find the same box, can be upgraded
        #                 for i in range(len(grid_x)):
        #                     if grid_x[i][0] == f1[0]:
        #                         grid_x[i][1] = br[0]
        #                         break
        #                 boxoption1 = deepcopy(obox)
        #                 boxoption1.remove(f1)

        #                 if f1 in line2:
        #                     line2.remove(f1)

        #                 for f2 in line2: # select a box in the first line
        #                     if solved == True:
        #                         break
        #                     # print('f2')
        #                     # print(f2)
        #                     # [[1,3],'o']
        #                     # change the box
        #                     # combination
        #                     grid_1 = deepcopy(grid_x)
        #                     # this part use a for loop to find the same box, can be upgraded
        #                     for i in range(len(grid_1)):
        #                         if grid_1[i][0] == f1[0]:
        #                             grid_1[i][1] = br[0]
        #                             break
        #                     boxoption = deepcopy(boxoption1)
        #                     boxoption.remove(f2)
                        
        #                     # print('grid_1')
        #                     # print(grid_1)
        #                     # print('boxoption')
        #                     # print(boxoption)
        #                     boxoption = list(itertools.combinations(boxoption, len(br)-1)) # after put first box, the rest available box


        #                     # variable used by code below
        #                     # box option; grid 1, 
        #                     # put the other boxes in
        #                     for box_op in range(len(boxoption)): # select an order of combination
        #                         if solved == True:
        #                             break
        #                         usedbox = [br[0]]
        #                         grid_2 = deepcopy(grid_1) # copy the grid with the first box put in
        #                         # record the used box
        #                         # update the grid
        #                         # print the grid


        #                         for box1 in range(len(br)-1):
        #                         # print('br =', br)
        #                         # print('boxoption[box_op]')
        #                         # print(boxoption[box_op])
        #                             for i in range(len(grid_2)):
        #                                 # print(1, grid_2[i][0])
        #                                 # print(2, boxoption[box_op][box1])
        #                                 if grid_2[i][0] == boxoption[box_op][box1][0]:
        #                                     grid_2[i][1] = br[box1+1]
        #                                     break
        #                             usedbox.append(br[box1+1])
        #                             # print('used box')
        #                             # print(usedbox)
        #                             # print('grid_2')
        #                             # print(grid_2)
        #                             l_start_points = read_bff(filename, 'sp')
        #                             end_points = read_bff(filename, 'ep')
        #                             gridpoints_2 = convert_box(grid_2)


        #                             if (test_solution(gridpoints_2,l_start_points, end_points, filename)):
        #                                 solved = True
        #                                 print(grid_2)

        #                                 boxop_left = [box3 for box3 in grid_2 if box3[1] == 'o']
                                        
        #                                 print(boxop_left)
        #                                 # print(usedbox)

        #                                 brleft = deepcopy(list(br))
        #                                 print(brleft)
        #                                 for i in usedbox:
        #                                     brleft.remove(i)
        #                                 # print(brleft)
        #                                 box_left = Bl + brleft
        #                                 print(box_left)
        #                                 grid_s1 = grid_2
        #                                 break
    '''
    if there are B block left, put them inside
    copy the grid solved
    assign B box
    testing
    grid_solved_final
    then final output
    '''
    if box_left == []:
        grid_3 = grid_s1
        print(grid_3)
        solution_output(grid_3,filename, dim=50, gap=5)
    else:    
        solved = False
        boxop_left = list(itertools.combinations(boxop_left,len(box_left)))
        for box_op1 in range(len(boxop_left)):
            if solved == True:
                break
            count = len(box_left)
            grid_3 = deepcopy(grid_s1)
            for box4 in range(len(box_left)):
                for i in range(len(grid_3)):
                    if grid_3[i][0] == boxop_left[box_op1][box4][0]:
                        grid_3[i][1]= box_left[box4]
                        count -= 1
                        if count == 0:
    
                            l_start_points = read_bff(filename, 'sp')
                            end_points = read_bff(filename, 'ep')
                            grid_final = convert_box(grid_3)
                            if (test_solution(grid_final,l_start_points, end_points, filename)):
                                solved = True
                                print(grid_3)
                                solution_output(grid_3,filename, dim=50, gap=5)                           
                                break
if __name__ == "__main__":
    # solve('yarn_5.bff')  # takes long time to solve
    # solve('showstopper_4.bff')  # solved
    # solve('dark_1.bff')  # solved
    # solve('mad_1.bff')  # solved
    # solve('mad_4.bff')  # solved
    # solve('tiny_5.bff')  # solved
    solve('numbered_6.bff')  # solved
    # solve('mad_7.bff')  # takes long time to solve
