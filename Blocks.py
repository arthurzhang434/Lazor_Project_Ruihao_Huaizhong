#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 11:07:10 2019

@author: huaizhong
""
This class contains the functions to account for blocks
"""
#import numpy as np
from copy import deepcopy
#test, first step of Mad7
#grid_points = [[[2,1],[-1,0],'o'], [[9,4],[0,-1],'x']]

grid_points = [[[1, 0], [0, -1], 'o'], [[0, 1], [-1, 0], 'o'], [[1, 2], [0, 1], 'o'], [[2, 1], [1, 0], 'o'], 
               [[3, 0], [0, -1], 'o'], [[2, 1], [-1, 0], 'o'], [[3, 2], [0, 1], 'o'], [[4, 1], [1, 0], 'o'], 
               [[5, 0], [0, -1], 'o'], [[4, 1], [-1, 0], 'o'], [[5, 2], [0, 1], 'o'], [[6, 1], [1, 0], 'o'], 
               [[7, 0], [0, -1], 'o'], [[6, 1], [-1, 0], 'o'], [[7, 2], [0, 1], 'o'], [[8, 1], [1, 0], 'o'], 
               [[9, 0], [0, -1], 'o'], [[8, 1], [-1, 0], 'o'], [[9, 2], [0, 1], 'o'], [[10, 1], [1, 0], 'o'], 
               [[1, 2], [0, -1], 'A'], [[0, 3], [-1, 0], 'A'], [[1, 4], [0, 1], 'A'], [[2, 3], [1, 0], 'A'], 
               [[3, 2], [0, -1], 'o'], [[2, 3], [-1, 0], 'o'], [[3, 4], [0, 1], 'o'], [[4, 3], [1, 0], 'o'], 
               [[5, 2], [0, -1], 'A'], [[4, 3], [-1, 0], 'A'], [[5, 4], [0, 1], 'A'], [[6, 3], [1, 0], 'A'], 
               [[7, 2], [0, -1], 'o'], [[6, 3], [-1, 0], 'o'], [[7, 4], [0, 1], 'o'], [[8, 3], [1, 0], 'o'], 
               [[9, 2], [0, -1], 'A'], [[8, 3], [-1, 0], 'A'], [[9, 4], [0, 1], 'A'], [[10, 3], [1, 0], 'A'], 
               [[1, 4], [0, -1], 'o'], [[0, 5], [-1, 0], 'o'], [[1, 6], [0, 1], 'o'], [[2, 5], [1, 0], 'o'], 
               [[3, 4], [0, -1], 'A'], [[2, 5], [-1, 0], 'A'], [[3, 6], [0, 1], 'A'], [[4, 5], [1, 0], 'A'], 
               [[5, 4], [0, -1], 'o'], [[4, 5], [-1, 0], 'o'], [[5, 6], [0, 1], 'o'], [[6, 5], [1, 0], 'o'], 
               [[7, 4], [0, -1], 'o'], [[6, 5], [-1, 0], 'o'], [[7, 6], [0, 1], 'o'], [[8, 5], [1, 0], 'o'], 
               [[9, 4], [0, -1], 'x'], [[8, 5], [-1, 0], 'x'], [[9, 6], [0, 1], 'x'], [[10, 5], [1, 0], 'x'], 
               [[1, 6], [0, -1], 'o'], [[0, 7], [-1, 0], 'o'], [[1, 8], [0, 1], 'o'], [[2, 7], [1, 0], 'o'], 
               [[3, 6], [0, -1], 'o'], [[2, 7], [-1, 0], 'o'], [[3, 8], [0, 1], 'o'], [[4, 7], [1, 0], 'o'], 
               [[5, 6], [0, -1], 'o'], [[4, 7], [-1, 0], 'o'], [[5, 8], [0, 1], 'o'], [[6, 7], [1, 0], 'o'], 
               [[7, 6], [0, -1], 'o'], [[6, 7], [-1, 0], 'o'], [[7, 8], [0, 1], 'o'], [[8, 7], [1, 0], 'o'], 
               [[9, 6], [0, -1], 'o'], [[8, 7], [-1, 0], 'o'], [[9, 8], [0, 1], 'o'], [[10, 7], [1, 0], 'o'],
               [[1, 8], [0, -1], 'o'], [[0, 9], [-1, 0], 'o'], [[1, 10], [0, 1], 'o'], [[2, 9], [1, 0], 'o'], 
               [[3, 8], [0, -1], 'o'], [[2, 9], [-1, 0], 'o'], [[3, 10], [0, 1], 'o'], [[4, 9], [1, 0], 'o'], 
               [[5, 8], [0, -1], 'A'], [[4, 9], [-1, 0], 'A'], [[5, 10], [0, 1], 'A'], [[6, 9], [1, 0], 'A'], 
               [[7, 8], [0, -1], 'o'], [[6, 9], [-1, 0], 'o'], [[7, 10], [0, 1], 'o'], [[8, 9], [1, 0], 'o'], 
               [[9, 8], [0, -1], 'A'], [[8, 9], [-1, 0], 'A'], [[9, 10], [0, 1], 'A'], [[10, 9], [1, 0], 'A']]

#grid_points = [[[2, 1], [-1, 0], 'o'], [[9, 4], [0, -1], 'x']]
l_start_points = [[[2, 1], [1, 1]], [[9, 4], [-1, 1]]]

#l_start_points = [[[5,0],[1,-1]],[[0,9],[-1,1]]]
end_points = [[6, 3], [6, 5], [6, 7], [2, 9], [9, 6]]

#l_start_points = [[[2,1],[1,1]],[[9,4],[-1,1]]]

class Block():
    
    def __init__(self, grid_point, l_start_point): 
        self.grid_point = grid_point
        self.l_start_point = l_start_point
        self.new_l1 = []
        self.new_l2 = []
        #print(self.grid_point[2])
        #print(self.l_start_point)
    
        if self.grid_point[2] == 'o' or 'x':
            self.new_l1 = self.l_start_point
        if self.grid_point[2] == 'A':
            self.new_l1 = self.reflect()
        if self.grid_point[2] == 'B':
            self.new_l1 = self.opaque()
        if self.grid_point[2]== 'C':
            self.new_l1, self.new_l2 = self.refract()
        #print(self.new_l1, self.new_l2)    
        
    
    def reflect(self):
        if self.grid_point[1][0] == 0:
            self.l_start_point[1][1] = -self.l_start_point[1][1]
            self.new_l1 = self.l_start_point
        if self.grid_point[1][0] != 0:
            self.l_start_point[1][0] = -self.l_start_point[1][0]
            self.new_l1 = self.l_start_point
        return self.new_l1
                    
    def refract(self):
        self.new_l2 = deepcopy(self.l_start_point)
        self.reflect()
        return self.new_l1, self.new_l2
        
    def opaque(self):
        self.l_start_point[1][0] = 0
        self.l_start_point[1][1] = 0
        self.new_l1 = self.l_start_point
        return self.new_l1
#Block(alist,blist)       
    
#def find_gp(filename, point):
def find_gp(grid, point):
    # filename: in which picture
    # point e.g. : [[2, 1[], [1, 1]]
    # grid point [[8, 9], [-1, 0], 'o']
    
    # change w, h
    #w, h = read_bff(filename, 'size')
    w, h = 5, 5
    gp = []
    #print(point[0][0],point[0][1])
    

    if point[0][0] > 0 and point[0][0] < 2*w and point[0][1] > 0 and point[0][1] < 2*h:
        #box = read_bff(filename, 'box')
        #grid = convert_box(filename)
        if point[0][0] % 2 == 0:
            face = [-point[1][0], 0]
        if point[0][0] % 2 != 0:
            face = [0, -point[1][1]]
        for i in range(len(grid)):
            if grid[i][0] == point[0] and grid[i][1] == face:
                gp = grid[i]
                break
        return gp
    if point[0][0] == 0 or point[0][0] == 2*w or point[0][1] == 0 or point[0][1] == 2*h:
        gp = [[],[],'B']
        return gp
    
 
#print(find_gp(grid_points,l_start_points))
    

def update_laser(grid_points, l_start_points):
    laser_out_points = []
    
    for i in range(len(l_start_points)):
        grid_point = find_gp(grid_points, l_start_points[i])
        #print(grid_point)
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
    
def test_solution(grid_points, l_start_points, end_points):
    laser_path_point = []
    laser_path_point1 = []
    same_xy = 0

    while len(l_start_points) > 0:
        laser_path_point = laser_path_point + deepcopy(l_start_points)
        #print(laser_path_point)
        l_start_points = update_laser(grid_points, l_start_points)
        #print(l_start_points)
    
    for i in range(len(laser_path_point)):
        #print(laser_path_point[i][0])
        laser_path_point1 = laser_path_point1 + [laser_path_point[i][0]]
        
    for j in range(len(end_points)):
        for k in range(len(laser_path_point1)):
            if end_points[j] == laser_path_point1[k]:
                same_xy = same_xy + 1
    #print(same_xy)
    if len(end_points) == same_xy:
        return True
    if len(end_points) != same_xy:
        return False
            

print(test_solution(grid_points,l_start_points, end_points))


            

    
    
    
        