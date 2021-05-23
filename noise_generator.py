import random
import copy

def cut_noise(noise, max_num, min_num):
    for i in range(len(noise)):
        for o in range(len(noise[0])):
            if noise[i][o] > max_num:
                noise[i][o] = max_num
            if noise[i][o] < min_num:
                noise[i][o] = min_num
    return noise

def ret_sun_map(noise):
    sun_map = copy.deepcopy(noise)
    for i in range(len(noise)):
        for o in range(len(noise[0])):
            sun_map[i][o] = int((noise[i][o]) / 10 + 1)
            if sun_map[i][o] > 16:
                sun_map[i][o] = 16
            elif sun_map[i][o] < 6:
                sun_map[i][o] = 0
    return sun_map  


def ret_min_map(noise):
    min_map = copy.deepcopy(noise)
    for i in range(len(noise)):
        for o in range(len(noise[0])):
            min_map[i][o] = 16 - int((noise[i][o]) / 10 + 1)
            if min_map[i][o] < 6:
                min_map[i][o] = 0
            elif min_map[i][o] > 16:
                min_map[i][o] = 16
    return min_map  

def create_noise(x, y, maxsize = 15): #This is my very old shit(around 10.2020)
    pixels = []
    ret = []
    for i in range(x+maxsize):
        pixels.append([])
        for o in range(y+maxsize):
            pixels[i].append(0)
            
    for i in range(x+maxsize):
        for o in range(y+maxsize):
            pixels[i][o] += random.randint(0,255) / (maxsize+1)
            
    for num in range(1,maxsize):
        for i in range(int((x+maxsize)/(num*2+1))):
            for o in range(int((y+maxsize)/(num*2+1))):
                randcolor = random.randint(0,255) / (maxsize+1)
                for xp in range(-1*num,num + 1):
                    for yp in range(-1*num,num + 1):
                        pixels[i*(num*2+1)+num+xp][o*(num*2+1)+num+yp] += randcolor
    
    for i in range(x):
        ret.append([])
        for o in range(y):
            ret[i].append(pixels[i][o])
    return ret

def AA(noise):
    for i in range(len(noise)-1):
        for o in range(len(noise[0])):
            noise[i][o] = (noise[i-1][o]+noise[i][o]+noise[i+1][o])/3              
    for i in range(len(noise)):
        for o in range(len(noise[0])-1):
            noise[i][o] = (noise[i][o-1]+noise[i][o]+noise[i][o+1])/3
    return noise

def round_(noise, round_num = 6):
    for i in range(len(noise)):
        for o in range(len(noise[0])):
            noise[i][o] = int(noise[i][o]/round_num)*round_num
    return noise

def inc_contrast(noise):
    for i in range(len(noise)):
        for o in range(len(noise[0])):
            noise[i][o] = (noise[i][o]/140)**1.5*140
            if noise[i][o] > 255:
                noise[i][o] = 255
    return noise