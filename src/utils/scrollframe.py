
import tkinter as tk


class VerticalScrolledFrame:
    """
    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    keyword arguments are passed to the underlying Canvas (eg width, height)
    """
    def __init__(self, master, **kwargs):
        self.outer = tk.Frame(master)

        self.canvas = tk.Canvas(self.outer, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.inner = tk.Frame(self.canvas)
        
        self.canvas_frame = self.canvas.create_window((4, 4), window=self.inner, anchor='nw')
        
        self.vsb = tk.Scrollbar(self.canvas, orient=tk.VERTICAL, command=self.canvas.yview)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)

        self.canvas.config(yscrollcommand=self.vsb.set)
        
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)

        self.inner.bind('<Configure>', self._on_frame_configure)
        self.canvas.bind("<Configure>", self._frame_width)
        
        
        self.outer_attr = set(dir(tk.Widget))
        self.frames = (self.inner, self.outer)
    

    def _frame_width(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)

    def __getattr__(self, item):
        """geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
        all other attributes (_w, children, etc) are passed to self.inner"""
        return getattr(self.frames[item in self.outer_attr], item)

    def _on_frame_configure(self, event):

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _bind_mouse(self, event=None):
        """mouse event bind does not work, so this hack allows the use of bind_all
        Linux uses Buttons, Windows/Mac uses MouseWheel"""
        
        for ev in ("<Button-4>", "<Button-5>", "<MouseWheel>"):
            self.canvas.bind_all(ev, self._on_mousewheel)

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units" )
        elif event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units" )

    def _unbind_mouse(self, event=None):
	    for ev in ("<Button-4>", "<Button-5>", "<MouseWheel>"):
		    self.canvas.unbind_all(ev)