import tkinter
import tkinter.filedialog
from PIL import Image, ImageTk
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
class MessageDialogue():
	def __init__(self,message,title):
		self.root = tkinter.Tk()
		self.root.title(title)
		self.message_label = tkinter.Label(self.root,text=message)
		self.message_label.grid(row=0,column=0)
		self.ok_button = tkinter.Button(self.root,text="Ok",command=lambda : self.root.destroy())
		self.ok_button.grid(row=1,column=0)
		self.root.mainloop()
class ScannerUI():
	def __init__(self,scanner):
		#scanner
		self.scanner = scanner
		#root window
		self.root = tkinter.Tk()
		self.root.title("simplescan v0.5")
		#scanner mode
		self.mode_select_frame = tkinter.LabelFrame(self.root,text="Select mode")
		self.mode_select_frame.grid(row=0,column=0)
		self.single_image_mode_button = tkinter.Button(self.mode_select_frame,text="Single image",command=lambda : self.select_mode(SingleImageModeUI))
		self.single_image_mode_button.grid(row=0,column=0)
		#scanner frame where the ui for scanning shows up
		self.scan_frame = tkinter.LabelFrame(self.root,text="Scaner")
		self.scan_frame.grid(row=1,column=0)
		self.select_mode(SingleImageModeUI) #select default mode as single image
		self.root.mainloop()
	def select_mode(self,mode_ui):
		self.scan_mode_ui = mode_ui(self.scan_frame,self.scanner)
class SingleImageModeUI():
	thumbnail_size = (565,800)
	def __init__(self,parent_widget,scanner):
		self.scanner = scanner
		self.currently_scanned_image: Image = None
		self.parent_widget = parent_widget
		self.scan_button = tkinter.Button(self.parent_widget,text="Scan",command=self.perform_scan)
		self.scan_button.grid(row=0,column=0)
		self.save_button = tkinter.Button(self.parent_widget,text="Save",command=self.save_image)
		self.save_button.grid(row=0,column=1)
		self.preview_label = tkinter.Label(self.parent_widget,text="Preview will appear once a scan has been performed")
		self.preview_label.grid(row=1,column=0,columnspan=2)
	def perform_scan(self):
		self.currently_scanned_image = self.scanner.scan()
		thumbnail = self.currently_scanned_image.copy()
		thumbnail.thumbnail(self.thumbnail_size)
		self.thumbnail_image=ImageTk.PhotoImage(thumbnail)
		self.preview_label.configure(image=self.thumbnail_image)
	def save_image(self):
		if self.currently_scanned_image == None:
			MessageDialogue("Please scan an image first","error")
			return
		filename_to_save_in = tkinter.filedialog.asksaveasfilename()
		self.currently_scanned_image.save(filename_to_save_in)
