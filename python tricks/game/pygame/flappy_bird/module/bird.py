import pygame

class Bird(object):
    """定义一个鸟类"""

    def __init__(self,img_locs):
        """定义初始化方法"""
        self.birdRect = pygame.Rect(65, 50, 50, 50)  # 鸟的矩形
        # 定义鸟的3种状态列表
        self.birdStatus = [*img_locs]
        self.status = 0      # 默认飞行状态
        self.birdX = 120     # 鸟所在X轴坐标,即是向右飞行的速度
        self.birdY = 350     # 鸟所在Y轴坐标,即上下飞行高度
        self.jump = False    # 默认情况小鸟自动降落
        self.jumpSpeed = 10  # 跳跃高度
        self.gravity = 5     # 重力
        self.dead = False    # 默认小鸟生命状态为活着

    def birdUpdate(self):
        if self.jump:
            # 小鸟跳跃
            self.jumpSpeed -= 1           # 速度递减，上升越来越慢
            self.birdY -= self.jumpSpeed  # 鸟Y轴坐标减小，小鸟上升
        else:
            # 小鸟坠落
            self.gravity += 0.2           # 重力递增，下降越来越快
            self.birdY += self.gravity    # 鸟Y轴坐标增加，小鸟下降
        self.birdRect[1] = self.birdY     # 更改Y轴位置

    def jump_up(self):
        self.jump = True  # 跳跃
        self.gravity = 5  # 重力
        self.jumpSpeed = 10  # 跳跃速度
