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

solution = [['o','o','C','o'],
       ['o','o','o','A'],
       ['A','o','o','o'],
       ['o','o','o','o']
       ] 

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
            

def solution_output(solution, dim=20, gap=2):
    
    w_blocks = len(solution[0])
    h_blocks = len(solution)
    size = (w_blocks*(dim+gap) + gap, h_blocks*(dim+gap) + gap)
    img = Image.new("RGB", size, color=colors['gap'])
    
    for y1, y2 in enumerate(solution):
        for x1, x2 in enumerate(y2):
            set_colors(img, x1, y1, dim, gap, colors[x2])
            
    img.save('Solution.png')
        
solution_output(solution)
    

