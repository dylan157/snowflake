#!/usr/bin/env python3
import os
os.environ.setdefault('PATH', '')
import pygame, sys, os
from random import randint
from datetime import datetime
import time, math, imageio

global error_message
error_message = ""

class image(object):
    def __init__(self, hex_add_1, hex_add_2, hex_add_3, size, curve, merge, random, width, height ):
        self.check = True
        self.error_message = ""
        try:
            self.hex_add_1 = int(hex_add_1)
            self.hex_add_2 = int(hex_add_2)
            self.hex_add_3 = int(hex_add_3)
            self.size = int(size)
            self.curve = int(curve)
            self.merge = int(merge)
            self.random = random
            self.check = True
            self.width = int(width)
            self.height = int(height)
            os.environ["SDL_VIDEODRIVER"] = "dummy"
            pygame.display.init()

            if self.height > 4000:
                self.height = 4000
            if self.width > 4000:
                self.width = 4000
            if self.height < 50:
                self.height = 50
            if self.width < 50:
                self.width = 50

            self.screen = pygame.display.set_mode((self.height, self.width))

        except:
            self.check = False
            self.error_message = ("Check failed: Hex addition invalid. randomising addition. Input: 1;"+str(hex_add_1)+" 2;"+str(hex_add_2)+" 3;"+str(hex_add_3)+" size;"+str(size))
            print (self.error_message)
            return 

        addition_limit = randint(2, 244)
        self.hex_values = []
        self.hex_additions = []
        if int(self.merge) > 0 and self.random and self.check:
            self.size = randint(3, 20)
            self.hex_values.append([randint(0, 20), randint(0, 20), randint(0, 20)])
            self.hex_additions.append([randint(1, addition_limit), randint(1, addition_limit), randint(1, addition_limit)])

            for images in range(self.merge):
                self.hex_values.append([randint(0, 20), randint(0, 20), randint(0, 20)])
                self.hex_additions.append([randint(1, addition_limit), randint(1, addition_limit), randint(1, addition_limit)])

        elif self.random:
            if int(self.merge) > 0:
                for images in range(self.merge):
                    self.size = randint(3, 20)
                    self.hex_values.append([randint(0, 20), randint(0, 20), randint(0, 20)])
                    self.hex_additions.append([randint(1, addition_limit), randint(1, addition_limit), randint(1, addition_limit)])

        else:
            if (self.check):
                self.hex_values.append([randint(0, 20), randint(0, 20), randint(0, 20)])
                self.hex_additions.append([self.hex_add_1, self.hex_add_2, self.hex_add_3])
                self.size = int(self.size)
                for images in range(self.merge):
                    self.size = randint(3, 20)
                    self.hex_values.append([randint(0, 20), randint(0, 20), randint(0, 20)])
                    self.hex_additions.append([randint(1, addition_limit), randint(1, addition_limit), randint(1, addition_limit)])


            else:
                self.size = randint(6, 20)
                self.hex_values.append([randint(0, 20), randint(0, 20), randint(0, 20)])
                self.hex_additions.append([randint(1, addition_limit), randint(1, addition_limit), randint(1, addition_limit)])
                self.error_message = ("Hex addition invalid. randomising addition. Input: 1;"+str(self.hex_add_1)+" 2;"+str(self.hex_add_2)+" 3;"+str(self.hex_add_3)+" size;"+str(self.size))
                for images in range(self.merge):
                    self.hex_values.append([randint(0, 20), randint(0, 20), randint(0, 20)])
                    self.hex_additions.append([randint(1, addition_limit), randint(1, addition_limit), randint(1, addition_limit)])
        return
        #self.generate()
        #print ("Hex addition invalid. randomising addition. Input: 1;"+str(self.hex_add_1)+" 2;"+str(self.hex_add_2)+" 3;"+str(self.hex_add_3)+" size;"+str(self.size))

    def generate(self):
        x = 0
        y = 0
        addition_limit = randint(2, 244)

        #pixel colors:
        #not needed--------------------------------------------------------------
        #not needed--------------------------------------------------------------




        #save_file_text is a string that will be saved with an image as a txt file. this allows you to re open the image with the load option or animate.

        save_file_text = str(self.size) + " " + str(self.width) + " " + str(self.height) + " "

        image_num = 0

        for pixel in range(int(self.width*self.height/self.size)):
            if image_num > len(self.hex_values)-1:
                image_num = 0
            
            if int(self.curve) > 0:
                final_hex_values = [self.hex_values[image_num][0], self.hex_values[image_num][1], self.hex_values[image_num][2]]
            else:
                final_hex_values = [self.hex_values[image_num][0]%255, self.hex_values[image_num][1]%255, self.hex_values[image_num][2]%255]

            self.hex_values[image_num][0] += self.hex_additions[image_num][0]
            self.hex_values[image_num][1] += self.hex_additions[image_num][1]
            self.hex_values[image_num][2] += self.hex_additions[image_num][2]

            if int(self.curve) > 0:
                if self.hex_values[image_num][0] >255:
                    self.hex_values[image_num][0] = randint(1, int(self.curve))
                if self.hex_values[image_num][1] >255:
                    self.hex_values[image_num][1] = randint(1, int(self.curve))
                if self.hex_values[image_num][2] >255:
                    self.hex_values[image_num][2] = randint(1, int(self.curve))
            if self.merge > 0:  
                image_num += 1

            save_file_text += str(final_hex_values[0]) +" "+ str(final_hex_values[1]) +" "+ str(final_hex_values[2])+" "
            if x < self.width: x += self.size
            else: 
                x = 0
                if y < self.height: y += self.size
                else: break
        draw(save_file_text, self.screen)
        pygame.display.update()

        filename = str(self.size)+"A"+str(self.hex_additions[0][0])+"_"+str(self.hex_additions[0][1])+"_"+str(self.hex_additions[0][2])+"B"+str(randint(0,255))
        print(filename+".png")
        pygame.image.save(self.screen, str(filename)+".png")
        return (filename+".png")



def draw(file, screen):
    if file == "":
        file = input("enter text file name: ")+".txt"
        try:
            a = open(file, "r")
            b = (a.read())
            b = b.split()
        except:
            print("file not found")
            return 0
    else: b = file.split()
    print(len(b)/3)
    print(g.width*g.height/g.size)
    size = int(b[0])
    res = width, height = int(b[1]), int(b[2])
    if screen == "":
        pygame.display.quit()
        screen = pygame.display.set_mode((res))
        pygame.display.set_caption("random bit gen")
        pygame.display.flip()
        pygame.display.update()

    if len(file) < 6:
        return 0

    x = 0
    y = 0
    counter = 3

    for p in range(10000000):
        try:
            final_hex_values = [int(b[counter]), int(b[counter+1]), int(b[counter+2])]
            pygame.draw.rect(screen, final_hex_values, [x, y, int(size), int(size)]) 
            counter += 3
            if x < width: x += size
            else: 
                x = 0
                if y < height: y += size
                else: 
                    pygame.display.update()
                    break
        except: break

#g = image(1, 10, 10, 1, 1, 4, False)
for x in sys.argv:
    print(x)
if len(sys.argv)>7:
    g = image(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9])
elif len(sys.argv)==5:
    g = image(1, 10, 10, 1, 1, 4, True, sys.argv[3], sys.argv[4])
else: g = image(1, 10, 10, 10, 1, 0, False, 1500, 1500)
	

g.generate()
