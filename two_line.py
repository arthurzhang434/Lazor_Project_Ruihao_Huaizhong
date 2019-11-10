if len(read_bff(filename, 'sp')) == 2:
        if solved == False:#while
            for br in refl: # select an order of A C arrangement
                    # select on and put in(save the box)
                for f1 in line1: # select a box in the first line
                    print('f1')
                    print(f1)
                    # [[1,3],'o']
                    # change the box
                    # combination
                    grid_1 = deepcopy(import_box)
                    # this part use a for loop to find the same box, can be upgraded
                    for i in range(len(grid_1)):
                        if grid_1[i][0] == f1[0]:
                            grid_1[i][1] = br[0]
                            break
                    boxoption = deepcopy(obox)
                    boxoption.remove(f1)
                    
                    print('grid_1')
                    print(grid_1)
                    print('boxoption')
                    print(boxoption)
                    boxoption = list(itertools.combinations(boxoption, len(br)-1)) # after put first box, the rest available box


                    # variable used by code below
                    # box option; grid 1, 
                    # put the other boxes in
                    for box_op in range(len(boxoption)): # select an order of combination
                        usedbox = [br[0]]
                        grid_2 = deepcopy(grid_1) # copy the grid with the first box put in
                        # record the used box
                        # update the grid
                        # print the grid
                        for box1 in range(len(br)-1):
                            print('br =', br)
                            print('boxoption[box_op]')
                            print(boxoption[box_op])
                            for i in range(len(grid_2)):
                                # print(1, grid_2[i][0])
                                # print(2, boxoption[box_op][box1])
                                if grid_2[i][0] == boxoption[box_op][box1][0]:
                                    grid_2[i][1] = br[box1+1]
                                    break
                            usedbox.append(br[box1+1])
                            print('used box')
                            print(usedbox)
                            print('i')
                            print(i)
                            print('grid_2')
                            print(grid_2)