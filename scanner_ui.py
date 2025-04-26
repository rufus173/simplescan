import tkinter
class ListboxDialogue():
	def __init__(self,list_to_select_from,title="Pick an option"):
		self.root = tkinter.Tk()
		self.root.title(title)
		self.listbox = tkinter.Listbox(self.root,selectmode=tkinter.SINGLE)
		self.listbox.insert(0,*list_to_select_from)
		#default option
		if len(list_to_select_from) > 0:
			self.listbox.activate(0)

		self.listbox.grid(row=0,column=0,sticky=tkinter.NSEW)
		self.select_button = tkinter.Button(self.root,text="select",command=lambda : self.select())
		self.select_button.grid(row=1,column=0)
		self.root.mainloop()
	def select(self):
		self.result = (self.listbox.get(self.listbox.curselection()),self.listbox.curselection()[0])
		self.root.destroy()

	def get_result(self):
		return self.result
