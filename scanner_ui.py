import tkinter
from functools import partial
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
class PDFModeUI():
	mode_name = "Multi image pdf"
	def __init__(self,parent_widget,scanner):
		self.scanner = scanner
		self.parent_widget = parent_widget
		self.scanned_images_list = []
		self.selected_page = None

		self.controls_frame = tkinter.LabelFrame(parent_widget,text="Controls")
		self.controls_frame.grid(row=0,column=0,columnspan=2)
		self.rescan_button = tkinter.Button(self.controls_frame,text="Rescan")
		self.rescan_button.grid(row=0,column=0)
		self.new_page_button = tkinter.Button(self.controls_frame,text="New page",command=self.new_page)
		self.new_page_button.grid(row=0,column=1)
		self.save_button = tkinter.Button(self.controls_frame,text="Save",command=self.save)
		self.save_button.grid(row=0,column=2)

		self.page_listbox = tkinter.Listbox(parent_widget,selectmode=tkinter.SINGLE)
		self.page_listbox.grid(row=1,column=0,sticky=tkinter.NSEW)
		self.page_listbox.bind("<<ListboxSelect>>",self.page_listbox_item_selected)
		
		self.preview_label = tkinter.Label(parent_widget,text="Press new page to start")
		self.preview_label.grid(row=1,column=1)
	def page_listbox_item_selected(self,event):
		self.selected_page = event.widget.curselection()[0]
		self.update_preview()
	def update_preview(self):
		thumbnail = self.scanned_images_list[self.selected_page].copy()
		thumbnail.thumbnail((800,800))
		self.current_preview_image = ImageTk.PhotoImage(thumbnail)
		self.preview_label.configure(image=self.current_preview_image)
	def update_page_listbox(self):
		self.page_listbox.delete(0,tkinter.END)
		self.page_listbox.insert(0,*[f"Page {i+1}" for i in range(len(self.scanned_images_list))])
	def new_page(self):
		self.scanned_images_list.append(self.scanner.scan())
		self.update_page_listbox()
		self.page_listbox.activate(tkinter.END)
		self.selected_page = len(self.scanned_images_list)-1
		self.update_preview()
	def save(self):
		if len(self.scanned_images_list) < 1:
			MessageDialogue("You need at least 1 scan to save","Error")
			return
		path = tkinter.filedialog.asksaveasfilename(defaultextension="pdf")
		self.scanned_images_list[0].save(path,"PDF",resolution=100.0,save_all=True,append_images=self.scanned_images_list[1:])
class SingleImageModeUI():
	mode_name = "Single image"
	thumbnail_size = (800,800)
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
		filename_to_save_in = tkinter.filedialog.asksaveasfilename(defaultextension="png")
		self.currently_scanned_image.save(filename_to_save_in)
class ScannerUI():
	scan_mode_uis = [PDFModeUI,SingleImageModeUI]
	def __init__(self,scanner):
		#scanner
		self.scanner = scanner
		#root window
		self.root = tkinter.Tk()
		self.root.title("simplescan v0.9")
		#scanner mode
		self.mode_select_frame = tkinter.LabelFrame(self.root,text="Select mode")
		self.mode_select_frame.grid(row=0,column=0)
		mode_buttons = [
			tkinter.Button(self.mode_select_frame,text=mode_ui.mode_name,command=partial(lambda ui: self.select_mode(ui),mode_ui))
			for mode_ui in self.scan_mode_uis
		]
		[mode_buttons[i].grid(row=0,column=i) for i in range(len(self.scan_mode_uis))]
		#scanner frame where the ui for scanning shows up
		self.scan_frame = tkinter.LabelFrame(self.root,text="Scaner")
		self.scan_frame.grid(row=1,column=0)
		self.scan_mode_ui = None
		self.root.mainloop()
	def select_mode(self,mode_ui):
		if self.scan_mode_ui != None:
			[slave.destroy() for slave in self.scan_frame.grid_slaves()]
			del self.scan_mode_ui
		self.scan_mode_ui = mode_ui(self.scan_frame,self.scanner)
