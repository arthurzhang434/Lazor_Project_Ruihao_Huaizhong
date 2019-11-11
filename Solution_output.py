#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 10:57:01 2019

@author: huaizhong
"""
'''
This file contains the function to visualize the output of the solution
'''
from PIL import Image

solution0 = [[[1, 1], 'o'], [[3, 1], 'o'], [[5, 1], 'C'], [[7, 1], 'o'], 
             [[1, 3], 'o'], [[3, 3], 'o'], [[5, 3], 'o'], [[7, 3], 'A'], 
             [[1, 5], 'A'], [[3, 5], 'o'], [[5, 5], 'o'], [[7, 5], 'o'], 
             [[1, 7], 'o'], [[3, 7], 'o'], [[5, 7], 'o'], [[7, 7], 'o']]


colors ={'o':(255,255,255),
         'x':(0,0,0),
         'A':(236,157,157),
         'B':(0,0,0),
         'C':(176,174,174),
         'gap':(255,1,1)
        }

def set_colors(img, x0, y0, dim, gap, color):
    for x in range(dim):
        for y in range(dim):
            img.putpixel((gap + (gap+dim)*x0 + x, gap + (gap+dim)*y0 + y),
                         color
                    )
            

def solution_output(solution0, dim=50, gap=5):
    solution1  = []
    solution2 = []
    x = 0
    for j in range(int(len(solution0)/4)):
        for i in range(int(len(solution0)/4)):
            solution1.append(solution0[4*x + i][1])
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
            
    #img.save('Solution.png')
        
solution_output(solution0)
   

