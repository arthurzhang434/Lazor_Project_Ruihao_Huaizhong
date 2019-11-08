def first_line():

	#use the initial condition to find the boxes on the line

def solve(import_box, nA = 11, nB = 0, nC = 0):

    # some trial on brute force to solve the maze is found to be impossible when
    # the overall block exceed 12, so we need some strategy when we try to put the 
    # ABC block on the availabe position on o.
    # the order of assigning the position: refract, reflect, then the opaque
    
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
