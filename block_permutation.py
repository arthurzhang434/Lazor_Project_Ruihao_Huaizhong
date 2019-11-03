def isswap(array,i,j):    # define a function to check whether swap is available
    if i == j:
        return True
    for n in range(i,j):
        if array[n][1] != array[j][1]:  
            continue
        else:  #  if there is element same as array j in this range 
            return False
    return True
 
def permutations(arr, begin = 0):
    end = len(arr)
    if begin == end:
        print(arr)
    else:
        for index in range(begin, end):
            if isswap(arr,begin,index):
                arr[index][1], arr[begin][1] = arr[begin][1], arr[index][1]
                permutations(arr, begin + 1)
                arr[index][1], arr[begin][1] = arr[begin][1], arr[index][1]
# reference:permutations and remove the repeat variants
#  https://blog.csdn.net/ggdhs/article/details/90285794

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
    
    for i in range(len(obox)):
        obox[i][1] = box_unp[i]
    
    permutations(obox)

    # Some problem when trying to return the value, can only print 

if __name__ == "__main__":
    box = [[(1, 1), 'o'], [(3, 1), 'o'], [(5, 1), 'o'], [(1, 3), 'o'], [(3, 3), 'x'], [(5, 3), 'x'], [(1, 5), 'o'], [(3, 5), 'o'], [(5, 5), 'o'], [(1, 7), 'o'], [(3, 7), 'x'], [(5, 7), 'o'], [(1, 9), 'o'], [(3, 9), 'o'], [(5, 9), 'o']]
    # permutations(['o','o', 'A', 'A', 'A', 'B', 'B'])
    box_permu(box) 

