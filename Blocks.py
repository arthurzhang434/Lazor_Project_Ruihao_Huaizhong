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

class Block():
    
    def __init__(self, grid_points, l_start_points): #type(grid_points,l_start_points)=np.array
        self.grid_points = grid_points
        self.l_start_points = l_start_points
        self.new_l = []
        for i in range(len(self.grid_points)):
            if self.grid_points[i][2] == 'o' or 'x':
                self.new_l.append(self.noblock(self.l_start_points, self.grid_points[i]))
            if self.grid_points[i][2] == 'A':
                self.new_l.append(self.reflect(self.l_start_points, self.grid_points[i]))
            if self.grid_points[i][2] == 'B':
                self.new_l.append(self.opaque())
            if self.grid_points[i][2]== 'C':
                #set 2 variables to account the 2 return values for refract function
                l1, l2 = self.refract(self.l_start_points, self.grid_points[i])
                self.new_l.append(l1)
                self.new_l.append(l2)
            

    def noblock(self, l_start_points, grid_point):
        old_l_points = deepcopy(self.l_start_points)
        for i in range(len(self.l_start_points)):
            if self.l_start_points[i][0] == grid_point[0]:
                self.l_start_points[i][0][0] == self.l_start_points[i][0][0] + self.l_start_points[i][1][0]
                self.l_start_points[i][0][1] == self.l_start_points[i][0][1] + self.l_start_points[i][1][1]
            else:
                continue
        if old_l_points == self.l_start_points:
            return None
        if old_l_points != self.l_start_points:
            return self.l_start_points
    
    def reflect(self, l_start_points, grid_point):
        old_l_points = deepcopy(self.l_start_points)
        for i in range(len(self.l_start_points)):
            if self.l_start_points[i][0][0] % 2 != 0:
                if self.l_start_points[i][0] == grid_point[0] and (self.l_start_points[i][1][1])*(grid_point[1][1])<0:
                    self.l_start_points[i][1][1] = -self.l_start_points[i][1][1]
                    self.l_start_points[i][0][0] = self.l_start_points[i][0][0] + self.l_start_points[i][1][0]
                    self.l_start_points[i][0][1] = self.l_start_points[i][0][1] + self.l_start_points[i][1][1]
            if self.l_start_points[i][0][0] % 2 == 0:
                if self.l_start_points[i][0] == grid_point[0] and (self.l_start_points[i][1][0])*(grid_point[1][0])<0:
                    self.l_start_points[i][1][0] = -self.l_start_points[i][1][0]
                    self.l_start_points[i][0][0] = self.l_start_points[i][0][0] + self.l_start_points[i][1][0]
                    self.l_start_points[i][0][1] = self.l_start_points[i][0][1] + self.l_start_points[i][1][1]
        if old_l_points == self.l_start_points:
            return None
        if old_l_points != self.l_start_points:
            return self.l_start_points
        
    def refract(self, l_start_points, grid_point):#set 2 return values, reflect and transmitt
        old_l_points1 = deepcopy(self.l_start_points)
        old_l_points2 = deepcopy(self.l_start_points)
        self.reflect()
        self.noblock()
        
    
    def opaque(self):
        return None
                    
        
            
            

        
                    
        
        
        
        

                            
                            
                                
                            
                            
                        
                    
                

                        
                    
        

    


        