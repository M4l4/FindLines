import matplotlib
matplotlib.use("TkAgg")     # Fixes error on OSX
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
import os
import re
from pathlib import Path
from PIL import Image, ImageTk
from FindErrors import find_errors
from skimage import io
from skimage.external import tifffile
from skimage.draw import line


class Main(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Find Errors")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        mainframe = ttk.Frame(self, padding="10")
        mainframe.grid(sticky=(N, W, E, S))
        mainframe.rowconfigure(1, weight=1, pad=5, minsize=50)
        mainframe.rowconfigure(3, pad=10)
        mainframe.columnconfigure(0, minsize=200)
        mainframe.columnconfigure(2, pad=5)
        mainframe.columnconfigure(4, weight=1)

        self.count = 0
        self.process = StringVar()
        self.process.set('None')
        self.bit_change = IntVar()
        self.bit_depth = IntVar()
        self.bit_var = 0
        self.otsu = IntVar()
        self.high = StringVar()
        self.low = StringVar()
        self.high.set(.9)
        self.low.set(.4)
        self.otsu.set(1)

        ttk.Label(mainframe, text="Processing:").grid(row=2, column=0, sticky=(W, S))
        ttk.Label(mainframe, textvariable=self.process).grid(row=2, column=1, sticky=S)

        self.files = []
        ttk.Button(mainframe, text="Select Directory", command=self.change_directory).grid(row=0, column=0, sticky=W)

        ttk.Button(mainframe, text="Options", command=self.pref).grid(row=0, column=1, sticky=E)

        fileframe = ttk.Labelframe(mainframe, text='Files:')
        fileframe.rowconfigure(0, pad=50)
        fileframe.grid(row=1, column=0, columnspan=2, sticky=(N, W, S, E))
        fileframe.grid_propagate(0)
        self.file_strings = StringVar()
        ttk.Label(fileframe, textvariable=self.file_strings).grid()

        ttk.Button(mainframe, text="Run", command=self.go).grid(row=1, column=2)
        ttk.Button(mainframe, text="Next", command=self.next_img).grid(row=1, column=3)

        canvasframe = ttk.Labelframe(mainframe)
        canvasframe.grid(row=1, column=4, rowspan=2, sticky=(N, W, S, E))
        canvasframe.rowconfigure(0, weight=1)
        canvasframe.columnconfigure(0, weight=1)

        xscrollbar = Scrollbar(canvasframe, orient=HORIZONTAL)
        xscrollbar.grid(row=1, column=0, sticky=(E, W))

        yscrollbar = Scrollbar(canvasframe)
        yscrollbar.grid(row=0, column=1, sticky=(N, S))

        self.canvas = Canvas(canvasframe, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        self.img_on_canvas = self.canvas.create_image(0, 0, anchor='nw')
        self.canvas.grid(row=0, column=0, sticky=(N, W, S, E))
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

        xscrollbar.configure(command=self.canvas.xview)
        yscrollbar.configure(command=self.canvas.yview)

        self.to_display = []
        self.images = []

        self.progress = ttk.Progressbar(mainframe, orient=HORIZONTAL, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=5, sticky=(E, W))

    def change_directory(self):
        self.files = []
        folder = askdirectory()
        for f in os.listdir(folder):
            if re.search('(?i)\.jpg', f):
                self.files.append(str(Path(folder+"\\"+f).resolve()))
        self.file_strings.set('\n'.join(self.files))
        self.count = 0

    def go(self):
        self.progress['maximum'] = len(self.files)
        self.progress['value'] = 0
        self.to_display = []
        for n, f in enumerate(self.files):
            self.process.set(f)
            self.update_idletasks()
            self.to_display.append([])
            try:
                self.to_display[n].append(find_errors(f, self.bit_var, self.otsu.get(), float(self.high.get()),
                                                      float(self.low.get())))
            except:
                raise
            self.progress['value'] += 1
        self.process.set('Rendering')
        # DONT TRY AND DISPLAY
        # for n, i in enumerate(self.files):
        #     image = io.imread(i)
        #     for j in self.to_display[n]:
        #         for k in j:
        #             p0, p1 = k
        #             rr, cc = line(p0[0], p0[1], p1[0], p1[1])
        #             image[rr, cc] = 255
        #     self.images.append(image)
        self.process.set('None')
        self.count = 1

    def next_img(self):
        if not self.count:
            pass
        else:
            if self.count > len(self.images):
                self.count = 1
            img = ImageTk.PhotoImage(Image.fromarray(self.images[self.count - 1]))
            self.canvas.itemconfig(self.img_on_canvas, image=img)
            self.canvas.img = img
            self.count += 1

    def pref(self):
        pref_win = Toplevel()
        pref_win.transient(self)
        pref_win.grab_set()
        pref_frame = ttk.Frame(pref_win, padding="10")
        pref_frame.grid(sticky=(N, W, E, S))
        bit_spin = Spinbox(pref_frame, from_=1, to=16, textvariable=self.bit_depth,
                           command=self.bit_var_change)
        if not self.bit_change.get():
            bit_spin['state'] = DISABLED
        bit_spin.grid(row=0, column=1, columnspan=2)
        ttk.Checkbutton(pref_frame, text="Reduce bit depth by", variable=self.bit_change,
                        command=lambda: self.swap_state(bit_spin)).grid(row=0, column=0, sticky=W)
        ttk.Radiobutton(pref_frame, text="Use Otsu's method to determine\nCanny thresholds (ratio between 0 - 1)",
                        variable=self.otsu, value=1).grid(row=1, column=0, sticky=W)
        ttk.Radiobutton(pref_frame, text="Set Canny thresholds manually (0 - 255)",
                        variable=self.otsu, value=0).grid(row=2, column=0, sticky=W)
        self.otsu.set(1)
        ttk.Label(pref_frame, text='Upper threshold').grid(row=1, column=1, sticky=W)
        ttk.Entry(pref_frame, width=3, textvariable=self.high).grid(row=1, column=2, sticky=W)
        ttk.Label(pref_frame, text='Lower threshold').grid(row=2, column=1, sticky=W)
        ttk.Entry(pref_frame, width=3, textvariable=self.low).grid(row=2, column=2, sticky=W)

    def bit_var_change(self):
        self.bit_var = self.bit_depth.get()

    def swap_state(self, widget):
        if widget['state'] == NORMAL:
            widget['state'] = DISABLED
            self.bit_var = 0
        else:
            widget['state'] = NORMAL
            self.bit_var = self.bit_depth.get()


if __name__ == "__main__":
    Main().mainloop()
