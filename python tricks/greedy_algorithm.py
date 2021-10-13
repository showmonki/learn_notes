unit_list = [1,5,10,20,25]
thre_num = 41

def max_first(unit_list, thre_num):
	sort_list = sorted(unit_list, reverse=True)
	sum_cookie = {k:0 for k in unit_list}
	iter_loop = 0
	while sum([k*v for k,v in sum_cookie.items()]) < thre_num:
		iter_loop +=1
		sum_gap = thre_num - sum([k*v for k,v in sum_cookie.items()])
		sum_cookie[max([v for v in sort_list  if v<=sum_gap])] +=1
		print(iter_loop,sum_cookie)


max_first(unit_list,thre_num)

# Reference:
# https://zhuanlan.zhihu.com/p/53334049
# https://blog.csdn.net/l2580258/article/details/63425301