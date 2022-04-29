import random

class Pipeline(object):
    """定义一个管道类"""

    def __init__(self,imgs):
        """定义初始化方法"""
        self.wallx = 400  # 管道所在X轴坐标
        self.pineUp = imgs[0]
        self.pineDown = imgs[1]
        self.loc_up = -300
        self.loc_down = 500

    def updatePipeline(self,score=0):
        """"管道移动方法"""
        pipeline_move = 5
        self.wallx -= pipeline_move  # 管道X轴坐标递减，即管道向左移动
        # 当管道运行到一定位置，即小鸟飞越管道，分数加1，并且重置管道
        if (100-pipeline_move)<= self.wallx < 100:
            score += 1
        if self.wallx < -80:
            self.wallx = 400
            self.pipe_loc_random()
        return score

    def pipe_loc_random(self):
        upper_loc = random.randrange(150,350)
        gap_pixel = random.randrange(150,250)
        self.loc_up = -500+upper_loc
        self.loc_down = upper_loc + gap_pixel
