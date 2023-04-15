"""
最初测试prompt：用python写一个在pygame界面的倒计时功能，界面有个开始按钮，鼠标点击开始后，才开始进行倒计时，并且在界面中心显示倒数，倒数结束后，显示游戏结束的文字和2个按钮，按钮1：重新开始，再次进入倒计时的流程， 按钮2： 结束，退出
prompt:
用python写一个在pygame界面的倒计时功能(默认5秒)
界面有个开始按钮，鼠标点击开始“Start”后，才开始进行倒计时（counter method），并且在界面中心显示倒数
倒数结束后，立马显示游戏结束的文字"Game Over"和2个按钮，按钮1：“Again”重新开始，重新显示倒计时主界面，再次进入倒计时的流程， 按钮2： "Exit"结束退出
流程：开始界面，Start按钮 -> counter method -> Game Over
Game Over: if Again, 重新跳回开始界面，If Exit, 退出
console log显示鼠标点击状态和倒计时的数字
按钮为抽取的method，属性为surface, 高宽设置为自动匹配显示文字的高度，按钮范围内均为有效点击区域
pygame 高640,宽480；字体颜色 白色，按钮颜色 灰色，背景为黑色

chatgpt 自动返回的功能描述：
这个代码中，我们创建了一个 Button 类来表示按钮，包含按钮的文本、位置、大小等信息，并且可以绘制按钮的表面和判断鼠标点击是否在按钮范围内。counter 方法实现了倒计时功能，计算倒计时的剩余时间，并且在界面中央显示剩余时间，同时处理事件和输出鼠标点击状态到console log。game_over 方法实现了游戏结束的界面，显示 "Game Over" 和两个按钮，处理事件并且输出鼠标点击状态到console log。在游戏循环中，我们创建了一个 "Start" 按钮，当鼠标点击 "Start" 按钮时，调用 counter 方法开始倒计时。如果倒计时结束，调用 game_over 方法显示游戏结束的界面。在游戏结束的界面中，如果点击了 "Again" 按钮，重新开始倒计时，如果点击了 "Exit" 按钮，退出游戏。同时，我们也输出了鼠标点击状态到console log。

"""

import pygame
import time

# 初始化pygame
pygame.init()
pygame.font.init()

# 定义常量
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BG_COLOR = (0, 0, 0)
FONT_COLOR = (255, 255, 255)
BUTTON_COLOR = (128, 128, 128)
COUNTDOWN_SECONDS = 5
RED = (255, 0, 0)

# 创建窗口
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Countdown Game")

# 创建字体
font = pygame.font.SysFont("Arial", 100)


# 定义按钮类
class Button:
	def __init__(self, text, x, y):
		self.text = text
		self.font = pygame.font.SysFont("Arial", 60)
		self.x = x
		self.y = y
		self.surface = self.font.render(self.text, True, FONT_COLOR)
		self.width = self.surface.get_width()
		self.height = self.surface.get_height()

	def draw(self):
		pygame.draw.rect(window, BUTTON_COLOR, (self.x, self.y, self.width, self.height))
		window.blit(self.surface, (self.x, self.y))

	def is_clicked(self, mouse_pos):
		x, y = mouse_pos
		return (x > self.x and x < self.x + self.width) and (y > self.y and y < self.y + self.height)


# 定义计时器方法
def counter():
	start_time = time.time()
	remaining_time = COUNTDOWN_SECONDS
	while remaining_time > 0:
		# 处理事件
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			# 输出鼠标点击状态到console log
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				print(f"Mouse clicked at ({mouse_pos[0]}, {mouse_pos[1]})")

		# 绘制界面
		window.fill(BG_COLOR)
		text_surface = font.render(str(remaining_time), True, FONT_COLOR)
		text_x = (WINDOW_WIDTH - text_surface.get_width()) / 2
		text_y = (WINDOW_HEIGHT - text_surface.get_height()) / 2
		window.blit(text_surface, (text_x, text_y))
		pygame.display.update()

		# 计算剩余时间
		remaining_time = COUNTDOWN_SECONDS - int(time.time() - start_time)

	# 倒计时结束
	game_over()


# 定义游戏结束方法
def game_over():
	while True:
		# 处理事件
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			# 输出鼠标点击状态到console log
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				print(f"Mouse clicked at ({mouse_pos[0]}, {mouse_pos[1]})")
				if again_button.is_clicked(mouse_pos):
					# 重新开始
					counter()
				elif exit_button.is_clicked(mouse_pos):
					# 退出游戏
					pygame.quit()
					quit()

		# 绘制界面
		window.fill(BG_COLOR)
		text_surface = font.render("Game Over", True, RED)
		text_x = (WINDOW_WIDTH - text_surface.get_width()) / 2
		text_y = (WINDOW_HEIGHT - text_surface.get_height()) / 2
		window.blit(text_surface, (text_x, text_y))
		again_button.draw()
		exit_button.draw()
		pygame.display.update()


# 创建开始按钮和重新开始按钮
start_button = Button("Start", (WINDOW_WIDTH - font.render("Start", True, FONT_COLOR).get_width()) / 2, 200)
again_button = Button("Again", 100, 300)
exit_button = Button("Exit", WINDOW_WIDTH - 100 - font.render("Exit", True, FONT_COLOR).get_width(), 300)

# 游戏循环
while True:
	# 处理事件
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

		# 输出鼠标点击状态到console log
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = pygame.mouse.get_pos()
			print(f"Mouse clicked at ({mouse_pos[0]}, {mouse_pos[1]})")
			if start_button.is_clicked(mouse_pos):
				# 开始倒计时
				counter()

	# 绘制界面
	window.fill(BG_COLOR)
	start_button.draw()
	pygame.display.update()
