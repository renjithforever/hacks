"""
Pi Runner
=========================
renjith 2014, renjithforever@gmail.com

___[ABOUT]______
a small app that was used in pi day (14th march )celebration at SCIS UOH.
Each participant must recite the digits of Pi from memeory, 
the digits are entered into the app and it shows if its correct.

___[REQUIREMENTS]___
*python with pygame!
*a file with some large number of digits of pi

___[USAGE]_____
python pi-runner.py

"""

import pygame,time
from pygame.locals import *

piDigitsData="pi_digits.dat"

WHITE=(255,255,255)
BLACK=(0,0,0)
GREEN=(0,255,0)
RED=(255,0,0)

pygame.init()
WIDTH=800
HEIGHT=600
screen=pygame.display.set_mode((WIDTH,HEIGHT))

tFontP=pygame.font.SysFont("FreeSans",340)
tFontI=pygame.font.SysFont("FreeSans",40)
tFontG=pygame.font.SysFont("FreeSans",300)
background=pygame.Surface(screen.get_size())
background=background.convert()
background.fill(WHITE)
screen.blit(background,(0,0))

piDigits=list(open(piDigitsData,"r").readline())
index=-1
d=''


def paint(t1,t2,t1Color):


	tObj1=tFontP.render(str(t1),1,t1Color)
	tObj2=tFontI.render(str(t2),1,BLACK)

	tObj1Pos=tObj1.get_rect()
	tObj1Pos.centerx=background.get_rect().centerx
	tObj1Pos.centery=background.get_rect().centery

	tObj2Pos=tObj2.get_rect()
	tObj2Pos.centerx=background.get_rect().centerx
	tObj2Pos.centery=background.get_rect().centery + HEIGHT*(3/8.0)

	screen.fill(WHITE) 
	screen.blit(tObj1,tObj1Pos) 
	screen.blit(tObj2,tObj2Pos)
	pygame.display.update()

paint("GO!","pi.pi..pi...",BLACK)


while True:

	for event in pygame.event.get():
		if event.type ==KEYDOWN:
			key_code=event.key
			
			if (key_code >=48 and key_code<=57):
				key=key_code - 48
			elif (key_code>=256 and key_code<=265):
				key=key_code -256
			else:
				continue

			d=str(key)
			index+=1
		
			if d==piDigits[index]:
				paint(d,index+1,GREEN)
			else:
				suffix=' DIGIT' if index==1 else " DIGITS"
				paint("!"+str(d),"YOUR MILAGE IS "+str(index)+suffix,RED)
				time.sleep(4)
				paint("GO!","pi.pi..pi...",BLACK)
				index=-1
				pygame.event.clear()

					
				



