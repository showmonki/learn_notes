'''
曲奇饼问题
碗1： 30 香草，10 曲奇
碗2： 20 香草，20 曲奇
前提：得到香草曲奇
问：来自碗1概率
'''
# 贝叶斯框架
from thinkbayes import Pmf


class Cookie(Pmf):

	def __init__(self, hypos):
		Pmf.__init__(self)
		for hypo in hypos:
			self.Set(hypo,1)
		self.Normalize() # 归一化

	def Update(self, data):
		for hypo in self.Values():
			like  = self.Likelihood(data, hypo)
			self.Mult(hypo, like)
		self.Normalize()

	mixed = {
		'Bowl1':dict(vanilla = 0.75, chocolate = 0.25), # 碗1的flavor分布
		'Bowl2':dict(vanilla = 0.5, chocolate = 0.5) # 碗2的flavor分布
	}

	def Likelihood(self, data, hypo):
		mix = self.mixed[hypo]
		like = mix[data]
		return like



if __name__ == '__main__':
	'''pmf = Pmf()
	pmf.Set('Bowl1',0.5)
	pmf.Set('Bowl2',0.5)
	# 先验概率
	
	pmf.Mult('Bowl1', 0.75)
	pmf.Mult('Bowl2', 0.5)
	# 拿到一块香草后更新
	'''

	hypos = ['Bowl1','Bowl2']
	pmf = Cookie(hypos)
	pmf.Update('vanilla') # 重点理解 概率更新

	for hypo, prob in pmf.Items(): # Items 在dict wrapper里
		print(hypo, prob)

	dataset = ['vanilla','chocolate','vanilla']
	for data in dataset:
		pmf.Update(data)

	for hypo, prob in pmf.Items(): # Items 在dict wrapper里
		print(hypo, prob)