"""
最初测试prompt：用python写一个在pygame界面的倒计时功能，界面有个开始按钮，鼠标点击开始后，才开始进行倒计时，并且在界面中心显示倒数，倒数结束后，显示游戏结束的文字和2个按钮，按钮1：重新开始，再次进入倒计时的流程， 按钮2： 结束，退出

"""

import pygame

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen = pygame.display.set_mode((640, 480))

# 设置字体
font = pygame.font.Font(None, 100)

# 设置颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)


# 定义倒计时函数
def countdown(number):
    for i in range(number, 0, -1):
        # 清空屏幕
        screen.fill(BLACK)

        # 渲染倒计时数字
        text = font.render(str(i), True, WHITE)
        text_rect = text.get_rect(center=screen.get_rect().center)
        screen.blit(text, text_rect)

        # 更新屏幕
        pygame.display.flip()

        # 等待1秒
        pygame.time.wait(1000)

    # 清空屏幕
    screen.fill(BLACK)

    # 渲染游戏结束文字
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=screen.get_rect().center)
    screen.blit(text, text_rect)

    # 渲染重新开始和结束按钮
    restart_text = font.render("Again", True, WHITE)
    restart_button = pygame.Rect(200, 300, restart_text.get_width()+20, restart_text.get_height()+20)
    restart_text_rect = restart_text.get_rect(center=restart_button.center)
    pygame.draw.rect(screen, GRAY, restart_button)
    screen.blit(restart_text, restart_text_rect)

    quit_text = font.render("Exit", True, WHITE)
    quit_button = pygame.Rect(400, 300, quit_text.get_width()+20, quit_text.get_height()+20)
    quit_text_rect = quit_text.get_rect(center=quit_button.center)
    pygame.draw.rect(screen, GRAY, quit_button)
    screen.blit(quit_text, quit_text_rect)

    # 更新屏幕
    pygame.display.flip()

    # 等待用户点击按钮
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(pos):
                    print('Again')
                    start_button_setup()
                    return True
                elif quit_button.collidepoint(pos):
                    print('Quit')
                    return False


# 渲染开始按钮
def start_button_setup():
    start_text = font.render("Start", True, WHITE)
    start_button = pygame.Rect(270, 200, start_text.get_width()+20, start_text.get_height()+20)
    start_text_rect = start_text.get_rect(center=start_button.center)
    pygame.draw.rect(screen, GRAY, start_button)
    screen.blit(start_text, start_text_rect)
    return start_button

start_button = start_button_setup()
# 更新屏幕
pygame.display.flip()

# 等待用户点击开始按钮
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if start_button.collidepoint(pos):
                # 开始倒计时
                if countdown(5):
                    # 重新开始
                    continue
                else:
                    # 退出游戏
                    pygame.quit()
                    exit()

        elif event.type == pygame.QUIT:
            # 退出游戏
            pygame.quit()
            exit()
