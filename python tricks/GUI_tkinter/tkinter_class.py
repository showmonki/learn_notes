from tkinter import *
from tkinter import messagebox


class tool:

	def __init__(self,param):
		root = Tk()
		root.title("Tool")
		root.geometry('600x200')
		menubar = Menu(root)
		menubar.add_command(label="About this tool")

		self.frame = Frame(root)
		self.frame.pack()
		# input
		Label(self.frame, text="原始描述:").grid(row=1,column=0, sticky=W)
		self.input_str = Entry(self.frame, width=20)
		self.input_str.grid(row=1, column=1, sticky=W)

		# output
		# Label(self.frame, text="输出结果:").grid(row=20, sticky=W)
		self.result = Entry(self.frame)
		self.result.place(x=10,y=10,width=40, height=50)
		self.result.grid(row=param[1][0], column=1,padx=10,pady=10,ipadx=20,ipady=30)
		self.button_element(*param,self.show_answer)
		# Label(self.frame, textvariable=self.result, width=20).grid(row=4, sticky=W)

		# output2
		# self.button_var(*param, self.label_answer)
		# Button(self.frame, text="运行", height=1, width=5, fg='red', command=self.show_answer).grid(row=30,column=0, sticky=W)
		Button(self.frame, text="退出", height=1, width=8, fg="red", command=root.quit).grid(row=30,column=1,sticky=E)

		root['menu'] = menubar
		root.mainloop()

	def button_var(self,label_txt,label_pos,button_txt,button_pos,button_func):
		self.result = StringVar()
		Label(self.frame, text=label_txt).grid(row=label_pos[0], column=label_pos[1], sticky=W)
		Button(self.frame, text=button_txt, command=button_func(self.result)).grid(row=button_pos[0], column=button_pos[1])
		Label(self.frame, textvariable=self.result, width=20).grid(row=label_pos[0]+2, sticky=W)


	def button_element(self,label_txt,label_pos,button_txt,button_pos,button_func):
		Label(self.frame, text=label_txt).grid(row=label_pos[0], column=label_pos[1], sticky=W)
		Button(self.frame, text=button_txt, command=button_func).grid(row=button_pos[0], column=button_pos[1])


	@staticmethod
	def run_method(input):
		return input

	def show_answer(self):
		self.result.insert(0, '{0},\ttest\n lin2'.format(self.input_str.get()))

	def label_answer(self,var):
		var.set('{0},\nlog: \n'.format(self.input_str.get(),var.get()))


if __name__ == '__main__':
	getfile_param = ["输出结果:",(2,0),"运行",(1,3)]
	app = tool(getfile_param)
	print('done')