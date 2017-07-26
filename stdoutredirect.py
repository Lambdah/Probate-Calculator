# Ref: https://stackoverflow.com/questions/18517084/how-to-redirect-stdout-to-a-tkinter-text-widget
class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')
