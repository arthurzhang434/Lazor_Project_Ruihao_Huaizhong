import itertools


def box_permu(import_box, nA = 11, nB = 0, nC = 0):
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
    box_str = ''.join(box_unp)

    
    
    # for i in range(len(obox)):
    #     obox[i][1] = box_unp[i]


    print(box_unp)
    print(box_str)

    # perm = list(set(itertools.permutations(box_str, 12 )))
    # print(perm)
    # Some problem when trying to return the value, can only print 

if __name__ == "__main__":
    box = [[(1, 1), 'o'], [(3, 1), 'o'], [(5, 1), 'o'], [(1, 3), 'o'], [(3, 3), 'x'], [(5, 3), 'x'], [(1, 5), 'o'], [(3, 5), 'o'], [(5, 5), 'o'], [(1, 7), 'o'], [(3, 7), 'x'], [(5, 7), 'o'], [(1, 9), 'o'], [(3, 9), 'o'], [(5, 9), 'o']]
    # box_permu(box) 
    # b = 'oAAA'
    a =list(set(itertools.permutations('ooooaa', 6)))
    print(a)
