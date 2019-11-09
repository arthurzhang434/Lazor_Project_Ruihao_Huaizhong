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
grid_points = [[[2,1],[-1,0],'o'], [[9,4],[0,-1],'x']]
l_start_points = [[[2,1],[1,1]],[[9,4],[-1,1]]]

class Block():
    
    def __init__(self, grid_point, l_start_point): 
        self.grid_point = grid_point
        self.l_start_point = l_start_point
        self.new_l1 = []
        self.new_l2 = []
        #print(self.grid_point[2])
    
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
        return None
#Block(alist,blist)       
    
#def find_gp(filename, point):
def find_gp(grid, point):
    # filename: in which picture
    # point e.g. : [[2, 1[], [1, 1]]
    # grid point [[8, 9], [-1, 0], 'o']
    
    # change w, h
    #w, h = read_bff(filename, 'size')
    w, h = 15, 15
    gp = []
    #print(point[0][0])

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
    else:
        return 'out'
                
#print(find_gp(grid_points,l_start_points))
    

def update_laser(grid_points, l_start_points):
    laser_out_points = []
    for i in range(len(l_start_points)):
        grid_point = find_gp(grid_points, l_start_points[i])
        #print(grid_point)
        a = Block(grid_point, l_start_points[i])
        new_l1 = a.new_l1
        new_l2 = a.new_l2
        if len(new_l1) != 0:
            new_l1[0][0] = new_l1[0][0] + new_l1[1][0]
            new_l1[0][1] = new_l1[0][1] + new_l1[1][1]            
            laser_out_points.append(new_l1)
        if len(new_l2) != 0:
            new_l2[0][0] = new_l2[0][0] + new_l2[1][0]
            new_l2[0][1] = new_l2[0][1] + new_l2[1][1]
            laser_out_points.append(new_l2)
            
    return(laser_out_points)
    
print(update_laser(grid_points, l_start_points))
        
    

        
            
            

        
                    
        
        
        
        

                            
                            
                                
                            
                            
                        
                    
                

                        
                    
        

    


        