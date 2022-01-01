import pygame
from pygame.image import load


class GameMenu(object):

	def __init__(self):
		self.start = True
		self.end = False
		self.start_pic = load("../assets/start.jpg")
		self.start_loc = 150,200
		self.end_pic = load("../assets/end.jpg")
		self.end_loc = 150,300
		self.bird_pic = load("../assets/bird0.png")
		self.bird_loc = 120,200

	def menu_start(self,screen,background):
		screen.fill((255, 255, 255))  # 填充颜色
		screen.blit(background, (0, 0))  # 填入到背景
		screen.blit(pygame.transform.scale(self.start_pic, (150, 40)), self.start_loc)
		screen.blit(pygame.transform.scale(self.end_pic, (150, 40)), self.end_loc)

	def move_button(self,status):
		if status == 'start':
			self.bird_loc = 120,200
			self.start = True
			self.end = False
		if status == 'end':
			self.bird_loc = 120,300
			self.start = False
			self.end = True

	def menu_update(self,event_keys,screen):
		if event_keys[pygame.K_UP]:
			self.move_button('start')
		if event_keys[pygame.K_DOWN]:
			self.move_button('end')
		screen.blit(self.bird_pic,self.bird_loc)
