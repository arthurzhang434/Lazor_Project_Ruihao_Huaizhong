'''
Finished by Ruihao
read the bff file

returned value:

box_ori two dimensional list
number of A, B, C: nA, nB, nC

start point
[(rx, ry), (vx, vy)] 

end point
(x,y)


'''
def read_bff(filename):
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
            box.append([(2 * x + 1, 2 * y + 1), box_raw[y][x]])

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

    # print(box_raw)
    # print(box)
    # print(nA, nB, nC)
    # print(start_point)
    # print(end_point)
    # print('_____')

    return box

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

#     [(gx, gy), (ox, oy), gridtype]


    box = read_bff(filename)
    grid_point = []
    for b in box:
        x, y = b[0]
        gridtype = b[1]
        u = [(x, y-1), (0, -1), gridtype]
        d = [(x, y+1), (0, 1), gridtype]
        l = [(x-1, y), (-1, 0), gridtype]
        r = [(x+1, y), (1, 0), gridtype]
        grid_point.append(u)
        grid_point.append(l)
        grid_point.append(d)
        grid_point.append(r)

    return grid_point    


if __name__ == "__main__":
    print(read_bff('mad_7.bff'))
    # print('_____')
    # print(convert_box('numbered_6.bff'))
    # read_bff('dark_1.bff')
    # read_bff('mad_1.bff')
    # read_bff('mad_4.bff')
    # print(read_bff('mad_7.bff'))
    # read_bff('showstopper_4.bff')
    # print(read_bff('tiny_5.bff'))
    # read_bff('yarn_5.bff')
