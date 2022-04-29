import sys
import time
import pygame
from pygame.image import load
from pipeline import Pipeline
from bird import Bird
from menu import GameMenu

class game(object):

	def __init__(self):
		pygame.init()                            # 初始化pygame
		pygame.font.init()                       # 初始化字体
		self.font = pygame.font.SysFont("Arial", 50)  # 设置字体和大小
		size = width, self.height = 400, 650          # 设置窗口
		self.screen = pygame.display.set_mode(size)   # 显示窗口
		self.clock = pygame.time.Clock()              # 设置时钟
		self.menu = GameMenu()
		self.background = load("../assets/background.png")  # 加载背景图片


	def load_img(self):
		piplineImgs = [load("../assets/top.png"),load("../assets/bottom.png")]
		birdImgs = [load("../assets/bird1.png"),load("../assets/bird2.png"),load("../assets/birddead.png")]
		return piplineImgs,birdImgs

	def createMap(self):
		"""定义创建地图的方法"""
		self.screen.fill((255, 255, 255))  # 填充颜色
		self.screen.blit(self.background, (0, 0))  # 填入到背景

		# 显示管道
		self.screen.blit(self.pipeline.pineUp, (self.pipeline.wallx, self.pipeline.loc_up))  # 上管道坐标位置
		self.screen.blit(self.pipeline.pineDown, (self.pipeline.wallx, self.pipeline.loc_down))  # 下管道坐标位置
		self.score = self.pipeline.updatePipeline(self.score)

		# 显示小鸟
		if self.bird.dead:  # 撞管道状态
			self.bird.status = 2
		elif self.bird.jump:  # 起飞状态
			self.bird.status = 1
		else:
			self.bird.status = 0
		self.screen.blit(self.bird.birdStatus[self.bird.status], (self.bird.birdX, self.bird.birdY))  # 设置小鸟的坐标
		self.bird.birdUpdate()  # 鸟移动
		# 显示分数
		self.screen.blit(self.font.render('Score:' + str(self.score), -1, (255, 255, 255)), (100, 50))  # 设置颜色及坐标位置
		pygame.display.update()  # 更新显示

	def checkDead(self):
		# 上方管子的矩形位置
		upRect = pygame.Rect(self.pipeline.wallx, -300,
		                     self.pipeline.pineUp.get_width() - 10,
		                     self.pipeline.pineUp.get_height())

		# 下方管子的矩形位置
		downRect = pygame.Rect(self.pipeline.wallx, 500,
		                       self.pipeline.pineDown.get_width() - 10,
		                       self.pipeline.pineDown.get_height())
		# 检测小鸟与上下方管子是否碰撞
		if upRect.colliderect(self.bird.birdRect) or downRect.colliderect(self.bird.birdRect):
			self.bird.dead = True
		# 检测小鸟是否飞出上下边界
		if not 0 < self.bird.birdRect[1] < self.height:
			self.bird.dead = True
			return True
		else:
			return False

	def start(self):
		p_img, b_img = self.load_img()
		self.pipeline = Pipeline(p_img)  # 实例化管道类
		self.bird = Bird(b_img)  # 实例化鸟类
		self.score = 0
		self.play()

	def play(self):
		# 轮询事件
		while True:
			self.clock.tick(60)  # 每秒执行60次
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.bird.dead:
					self.bird.jump_up()
				# print(self.pipeline.loc_up,self.pipeline.loc_down)
			if self.checkDead():
				self.end()
			else:
				self.createMap()

	def run(self):
		while True:
			self.menu.menu_start(self.screen,self.background)
			self.screen.blit(self.menu.bird_pic,self.menu.bird_loc)
			pygame.display.flip()
			self.clock.tick(60)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					event_keys = pygame.key.get_pressed()
					self.menu.menu_update(event_keys,self.screen)
					pygame.display.flip()
					if event_keys[pygame.K_RETURN]:
						if self.menu.start:
							self.start()
						if self.menu.end:
							sys.exit()

	def end(self):
		final_text1 = "Game Over"
		ft1_font = pygame.font.SysFont("Arial", 48)  # 设置第一行文字字体
		ft1_surf = ft1_font.render(final_text1, 1, (242, 3, 36))  # 设置第一行文字颜色
		ft2_font = pygame.font.SysFont("Arial", 28)  # 设置第二行文字字体
		final_text2 = "Press m for menu"
		ft2_surf = ft2_font.render(final_text2, True, (253, 177, 6))  # 设置第二行文字颜色
		self.screen.blit(ft1_surf, [self.screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])  # 设置第一行文字显示位置
		self.screen.blit(ft2_surf, [self.screen.get_width() / 2 - ft2_surf.get_width() / 2, 400])  # 设置第二行文字显示位置
		pygame.display.flip()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					event_keys = pygame.key.get_pressed()
					if event_keys[pygame.K_m]:
						self.run()

if __name__ == '__main__':
	game().run()
