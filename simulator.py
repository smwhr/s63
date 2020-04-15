import tkinter as tk

class Led(object):
  def __init__(self):
      self._color = (0.0,0.0,0.0)
      self._hex   = "#000000"
      self.on_color_change = lambda: None

  def update_color(self):
    self._hex = "#"+"".join([hex(int(h*255))[2:].zfill(2) for h in self._color]).upper()
    self.on_color_change(self._hex)

  @property
  def color(self):
      return self._color

  @property
  def red(self):
      return self._color[0]

  @property
  def green(self):
      return self._color[1]

  @property
  def blue(self):
      return self._color[2]

  @color.setter
  def color(self, value):
      self._color = value
      self.update_color()

  @red.setter
  def red(self, value):
      self._color = (value, self.green, self.blue)
      self.update_color()

  @green.setter
  def green(self, value):
      self._color = (self.red, value, self.blue)
      self.update_color()

  @blue.setter
  def blue(self, value):
      self._color = (self.red, self.green, value)
      self.update_color()

class S63(tk.Tk):

    def __init__(self,master=None):
        tk.Tk.__init__(self,master)
        self.title("S63 Simulator")
        self.overrideredirect(True)
        self._offsetx = 0
        self._offsety = 0
        self.bind('<Button-1>',self.clickwin)
        self.bind('<B1-Motion>',self.dragwin)
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparent", True)
        self.config(bg='systemTransparent')
        self.geometry('+525+150')
        self.geometry('390x650')

        self.init_callbacks()
        self.init_hanger()
        self.init_buttons()
        self.init_led()

    def init_callbacks(self):
        self.comb_when_pressed = lambda: None
        self.comb_when_released = lambda: None
        self.on_compose = lambda: None

    def init_hanger(self):
      self.comb_hang = False
      comb_up = tk.PhotoImage(file="./assets/hanger_up.png").zoom(2,2).subsample(3, 3)
      comb_down = tk.PhotoImage(file="./assets/hanger_down.png").zoom(2,2).subsample(3, 3)
      def hang():
        if self.comb_hang:
            comb.configure(image=comb_down)
            print("Phone is unavailable")
            self.comb_when_released()
        else:
            comb.configure(image=comb_up)
            print("Phone is available")
            self.comb_when_pressed()
        self.comb_hang = not self.comb_hang

      comb = tk.Button(self, command=hang, image=comb_down)
      comb.grid(column=0, row=0, columnspan = 3)

    def init_buttons(self):
      self.digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '''#''']
      self.digit_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'star', '0', 'hash']
      self.digit_photos = [tk.PhotoImage(
          file="./assets/button_"+name+"_up.png").subsample(2, 2) for name in self.digit_names]
      for dig in enumerate(zip(self.digits, self.digit_names, self.digit_photos)):
          i, (lbl, name, photo) = dig

          def cb(lbl=lbl): return self.on_compose(lbl)
          btn = tk.Button(self, text=lbl, command=cb, image=photo)
          btn.grid(column=i % 3, row=i//3+2)

    def init_led(self):
      self.led = Led()
      self._canvas = tk.Canvas(self, width=385, height=100)
      self._canvas.grid(column=0, row=1, columnspan = 3)
      self._led_rectangle = self._canvas.create_rectangle(2, 2, 387, 99, fill="#f6e5d2", outline='')

      self.led.on_color_change = self.led_change

    def led_change(self, hexcolor):
      self._canvas.itemconfig(self._led_rectangle, fill=hexcolor)

    def dragwin(self,event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self._offsetx = event.x
        self._offsety = event.y

    def run(self):
        self.mainloop()
