from scanner import SaneScanner
from scanner_ui import *
import sane
if __name__ == "__main__":
	sane.init()
	print("starting sane...")
	device_list = sane.get_devices()
	scanner_name_list = [f"({l[0]}) {l[1]} - {l[2]}" for l in device_list]
	print(device_list)
	print("please choose a scanner")
	scanner_name, i = ListboxDialogue(scanner_name_list,title="Choose a scanner").get_result()
	scanner = SaneScanner(device_list[i][0])
	sane.exit()
