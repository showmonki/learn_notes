# Coin
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

# backpack
iter_list = [[4,13],[3,4],[8,5],[9,10],[7,11]]
max_num = 19
# capacity
def greedy_capacity(iter_list, max_n):
	iter_dict = {v:w for w,v in iter_list}
	iter_dict_sort = {v:iter_dict[v] for v in sorted(iter_dict,reverse=True)}
	sum_cookie = 0
	value_sum = 0
	iter_select = []
	for v,w in iter_dict_sort.items():
		if sum_cookie + w > max_n:
			pass
		else:
			sum_cookie += w
			value_sum += v
			iter_select.append([w,v])
	print(iter_select)
	print(sum([item[1] for item in iter_select]))

greedy_capacity(iter_list,max_num)