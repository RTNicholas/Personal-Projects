import tkinter as tk
import tkinter.ttk as ttk


class TkinterTools:

    @staticmethod
    def gui_position(window, title, width, height, x_add=0, y_add=0):
        # App title
        window.title(title)

        # Offset
        x_off = window.winfo_rootx() - window.winfo_x()  # Horizontal pixel offset
        y_off = window.winfo_rooty() - window.winfo_y()  # Vertical pixel offset

        # Top left (x,y) of pixel for application in centre of screen
        x = (window.winfo_screenwidth() - width - x_off) // 2 + x_add
        y = (window.winfo_screenheight() - height - y_off) // 2 + y_add

        # Apply application position
        window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    @staticmethod
    def make_treeview(root, column_list, align=tk.CENTER):
        w = ttk.Treeview(root,
                         columns=column_list, displaycolumns="#all"
                         )
        w.column('#0', width=0, stretch=tk.NO)

        for item in column_list:
            w.heading(item, text=item)
            w.column(item,anchor=align)

        return w


    @staticmethod
    def limit_entry(str_var, length):
        def callback(str_var):
            c = str_var.get()[0:length]
            str_var.set(c)

        str_var.trace("w", lambda name, index, mode, str_var=str_var: callback(str_var))

    @staticmethod
    def set_grid_config(widget, rc, rc_index="all", weights=1, propagate=True):

        rows = widget.grid_size()[1]
        cols = widget.grid_size()[0]
        size = max(rows, cols) if rc_index == "all" else len(rc_index)

        widget.grid_propagate(propagate)
        for i in range(size):

            weight_val = weights[i] if isinstance(weights, list) else weights
            indexer = i if rc_index == "all" else rc_index[i]

            if "r" in rc and i < rows and (rc_index == "all" or indexer in rc_index):
                widget.rowconfigure(indexer, weight=weight_val)

            if "c" in rc and i < cols and (rc_index == "all" or indexer in rc_index):
                widget.columnconfigure(indexer, weight=weight_val)

    @staticmethod
    def grid_label_entry(lbl, txt, row, col, padx=0, pady=0):

        lbl.grid(row=row, column=col, sticky=tk.E, padx=(padx, 0), pady=pady)
        txt.grid(row=row, column=col + 1, sticky=tk.EW, pady=pady, padx=(0, padx))

    # Alternate state
    @staticmethod
    def toggle_state(widget):
        # Reference of states
        states = {"normal": "disabled", "disabled": "normal"}

        # Update State
        widget.config(state=states[widget.cget("state")])

    # Alternate colours in order of list
    @staticmethod
    def change_colour(widget, colours):
        try:
            next_colour = colours[colours.index(widget.cget("bg")) + 1 % len(colours)]
        except:
            next_colour = colours[0]
        widget.config(bg=[next_colour])
