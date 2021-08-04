from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
from pandas.core.frame import DataFrame
from pandas.io.parsers import read_csv
from pandas.io.excel import read_excel
import os


def get_folder():
	global path_of_files_to_link
	path_of_files_to_link = filedialog.askdirectory()
	var.set(path_of_files_to_link)


def get_file():
	global cell_link_tool
	cell_link_tool = filedialog.askopenfilename()
	var1.set(cell_link_tool)


def output_file():
	# print("Running")
	# print(path_of_files_to_link)
	files = os.listdir(path_of_files_to_link)
	df = DataFrame()
	# print(df.head())
	if cell_or_item == 1:
		for file in files:
			data = read_csv(path_of_files_to_link + "/" + file,
			                names=['periodcode', 'categorycode', 'cellcode', 'storecode', 'wgt', 'cnt', 'rawvol',
			                       'pvol', 'pval', 'pstk', 'MBDCODE', 'TAGCODE'])
			df = df.append(data)
		tool = read_excel(cell_link_tool, sheetname="cell info")
		print(tool.head())
		data = DataFrame.merge(df, tool[
			['REGION', 'PROVINCE', 'CLASS2', 'TYPECODE', 'TYPE_DESC', 'STORETYPECODE', 'CELLCODE_MER', 'CHAIN_CN',
			 'CHAIN_EN', 'CELLCODE']], how="left", left_on="cellcode", right_on="CELLCODE")
		del data['CELLCODE']
		data.rename(columns={'CELLCODE_MER': 'CELLCODE', 'CLASS2': 'CLASS'})
		# print("Output")
		# print(data.head())
		data.to_excel(path_of_files_to_link + " cell list.xlsx", sheet_name="Cell list")
		tkinter.messagebox.showinfo('提示', '合并完毕')
	# print("Done")
	else:
		for file in files:
			data = read_csv(path_of_files_to_link + "/" + file,
			                names=['MBDcode', 'tagcode', 'period', 'category', 'cellcode', 'store code', 'wgt',
			                       'itemcode', 'price', 'sales unit', 'RAWVOL', 'ProjVOL', 'ProjValue', 'PSTOCK',
			                       'brand', 'LongDes'], encoding="ANSI")
			df = df.append(data)
		tool = read_excel(cell_link_tool, sheetname="cell info")
		data = DataFrame.merge(df, tool[
			['REGION', 'PROVINCE', 'CLASS2', 'TYPECODE', 'TYPE_DESC', 'STORETYPECODE', 'CELLCODE_MER', 'CHAIN_CN',
			 'CHAIN_EN', 'CELLCODE']], how="left", left_on="cellcode", right_on="CELLCODE")
		del data['CELLCODE']
		data.rename(columns={'CLASS2': 'CLASS'})
		# print("Output")
		data.to_excel(path_of_files_to_link + "item list.xlsx", sheet_name="Item list")
		tkinter.messagebox.showinfo('提示', '合并完毕')
	# print("Done")


def load_yaml(file_name):
	import yaml
	with open(file_name, 'r') as f:
		return yaml.load(f)


def gui_main():
	root = Tk()
	root.title("Tool")

	menubar = Menu(root)
	menubar.add_command(label="About this tool")

	frame = Frame(root)
	frame.pack()

	# label block 1
	Label(frame, text="选择csv存放文件夹（解压到单独一个文件夹、或单独放一个文件夹）:").grid(row=1, column=0, sticky=W)
	Button(frame, text="路径选择", command=get_folder).grid(row=1, column=26)
	var = StringVar()
	Label(frame, textvariable=var, bd=1, width=50).grid(row=2, sticky=W)

	# label block 2
	Label(frame, text="选择cell link tool（Excel文件）:").grid(row=3, column=0, sticky=W)
	Button(frame, text="打开文件", command=get_file).grid(row=3, column=26)
	var1 = StringVar()
	Label(frame, textvariable=var1, width=50).grid(row=4, sticky=W)

	v = IntVar()
	Label(frame, text="勾选csv文件类型:").grid(row=15, sticky=W)
	Radiobutton(frame, text="Cell list", variable=v, value=1, command=cell_or_item_click).grid(row=15, column=1,
	                                                                                           sticky=W)
	Radiobutton(frame, text="Item list", variable=v, value=2, command=cell_or_item_click).grid(row=15, column=2,
	                                                                                           sticky=E)

	Label(frame, text="*文件将输出到csv存放文件夹").grid(row=20, sticky=W)
	Button(frame, text="运行", height=1, width=5, fg='red', command=output_file).grid(row=20, sticky=E)

	Button(frame, text="退出", command=root.quit, height=1, width=8, fg="red").grid(row=40)

	root['menu'] = menubar
	root.mainloop()


if __name__ == '__main__':
	filename = './config.yaml'
	test = load_yaml(filename)
# csv_frame = Frame(frame)
# Label(csv_frame, text="选择cell、item list csv存放文件夹:",width=25).pack(side=LEFT)
# path_of_files_to_link = Button(csv_frame, text="路径选择", command=get_folder).pack(side=LEFT)
# var = StringVar()
# Label(csv_frame,textvariable=var,bd=1,width=30).pack(expand=1)
# csv_frame.pack()

# t_frame=Frame(frame)
# Label(t_frame, text="选择cell link tool excel:",width=25).pack(side=LEFT)
# cell_link_tool = Button(t_frame, text="打开文件", command=get_file).pack(side=LEFT)
# var1 = StringVar()
# Label(t_frame,textvariable=var1,width=30).pack()
# t_frame.pack()
