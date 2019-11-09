# Lazor Project
'''
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

'''
Finished by Ruihao
read the bff file

returned value:

box_ori two dimensional list
number of A, B, C: nA, nB, nC

start point
[[rx, ry], [vx, vy)] 

end point
(x,y)

'''
def read_bff(filename, select):
    fi = open(filename, 'r')
    bff = fi.read()
    line_split = bff.strip().split('\r\n')

    box_raw = [] 
    box = []
    start_point = []
    end_point = []

# convert the box text into a 2D list
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

            start_point.append([(int(s_p[1]),int(s_p[2]) ),((int(s_p[3])),int(s_p[4]))])

        elif line.startswith('P'):
            end_point.append((int(line[2]),int(line[4])))

    w = len(box_raw[0])
    h = len(box_raw)        

    
    # print('box_raw')
    # print(box_raw)
    # print('w,h')
    # print(w,h)
    # print('box')
    # print(box)
    # print('nA, nB, nC')
    # print(nA, nB, nC)
    print('start_point')
    print(start_point)
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

'''
convert the box to grid point with the type
'''
def convert_box(filename):

# (2) orientation (ox, oy): 
#     up (0, -1) / down (0,1) / left (-1, 0) / right (1, 0)

#     (3) type: o/ A/ B/ C
#     o: pass the point
#     A: reflect
#     B: terminate the ray
#     C: pass and reflect
#     convert [[cx,cy], gridtype] to
#     [[gx, gy], [ox, oy], gridtype]


    box = read_bff(filename, 'box')
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
#     convert [[gx, gy], [ox, oy], gridtype]  to
#     [[cx,cy], gridtype]
    if grid[1] == [-1, 0]:
        return [[grid[0][0] + 1, grid[0][1]], grid[2]]
    if grid[1] == [1, 0]:
        return [[grid[0][0] - 1, grid[0][1]], grid[2]]
    if grid[1] == [0, -1]:
        return [[grid[0][0], grid[0][1] + 1], grid[2]]
    if grid[1] == [0, 1]:
        return [[grid[0][0], grid[0][1] - 1], grid[2]]


# given a incident ray, find the grid point that face to the ray (can reflect)

def find_gp(point, filename):
    # filename: in which picture
    # point e.g. : [(2, 1), (1, 1)]
    # grid point [[8, 9], [-1, 0], 'o']
    
    # change w, h
    w, h = read_bff(filename, 'size')

    if point[0][0] < 0 or point[0][0] > 2 * w or point[0][1] < 0 or point[0][1] > 2 * h:
        print('error, out of range')
        return None
    else:    
        box = read_bff(filename, 'box')
        grid = convert_box(filename)
        if point[0][0] % 2 == 0:
            face = [-point[1][0], 0]
        else:
            face = [0, -point[1][1]]
        for i in range(len(grid)):
            if grid[i][0] == list(point[0]):
                if grid[i][1] == face:
                    gp = grid [i]
        return gp                

def first_line(n, filename): # also need to add start point
    # use the initial condition to find the boxes on the line
    # n can be 1 or 2 generate line for first or second line 
    box = read_bff(filename, 'box')
    start_point = [[(2, 1), (1, 1)], [(9, 4), (-1, 1)]]
    ponline = list(start_point[n-1])
    path = []
    while True:
        ponline

 
    self.l_start_points[i][0][0] == self.l_start_points[i][0][0] + self.l_start_points[i][1][0]
    self.l_start_points[i][0][1] == self.l_start_points[i][0][1] + self.l_start_points[i][1][1]
    pass

def solve(import_box, nA = 11, nB = 0, nC = 0):
    pass

    # some trial on brute force to solve the maze is found to be impossible when
    # the overall block exceed 12, so we need some strategy when we try to put the 
    # ABC block on the availabe position on o.
    # the order of assigning the position: refract, reflect, then the opaque
    '''
    import_box, nA = 6, nB = 0, nC = 0:
    obox = []
    for i in import_box:
        if i[1] == 'o':
            obox.append(i)

    no = len(obox) - nA - nB - nC
    box_unp, ol, Al, Bl, Cl = [], [], [], [], []

    if no:
        ol = ['o'] * no
    if nA:
        Al = ['A'] * nA
    if nB:
        Bl = ['B'] * nB
    if nC:
        Cl = ['C'] * nC          
    box_unp = ol + Al + Bl + Cl
'''


if __name__ == "__main__":
    a = convert_box('mad_7.bff')
    print(a)
    # b = [(1, 2), (1, 1)]
    # print(find_gp(b, 'mad_7.bff'))
    # c = first_line(1, 'mad_7.bff')


    # for i in range(len(a)):
    #     print(convert_grid(a[i]))

