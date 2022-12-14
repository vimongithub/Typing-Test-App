from tkinter import *
import tkinter
import ctypes
import random
import pandas

# Sharper window
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class TypingApp(Tk):
    def __init__(self):
        super().__init__()

        self.window_create()

    def window_create(self):
        self.geometry('1000x650+180+20')
        self.title("Typing Test")
        self.configure(bg='LightCyan4')

        fevicon = PhotoImage(file='images/fevicon.png')
        self.iconphoto(False,fevicon)

        self.option_add("*Label.Font", "consolas 30")
        self.option_add("*Button.Font", "consolas 30")
        self.home_screen()

    def home_screen(self):
        logo_img=PhotoImage(file='images/logo.png')
        bg_img = PhotoImage(file='images/home_screen.png')


        self.home_bg = Label(self, image=bg_img)
        self.home_bg.image =bg_img
        self.home_bg.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.logo = Label(self, image=logo_img, bg='LightCyan4')
        self.logo.image = logo_img

        #start button

        self.start_btn = Button(self, text="START NOW", fg='white', bg='Chocolate3', highlightcolor='PaleGreen4', command=self.test_start_msg)
        self.start_btn.place(relx=0.5, rely=0.7, anchor=N)

    def test_start_msg(self):

        self.home_bg.destroy()
        self.start_btn.destroy()

        self.logo.place(relx=0.3, rely=0.1, anchor=E)

        self.start_msg_label = Label(self, text='Starting Test...', fg='white', bg='LightCyan4',font=('consolas', 50, 'bold'))
        self.start_msg_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.after(2000, self.create_widgets)


    def create_widgets(self):
        self.start_msg_label.destroy()

        self.is_typing = True
        self.passed_seconds = 0
        self.typo_mistake = 0

        data = pandas.read_csv(filepath_or_buffer='paragraphs/paragraph_list.csv', index_col=False)
        paragraph_list = data['paragraphs'].tolist()
        text = random.choice(paragraph_list).lower()

        next_char = 0

        self.timer_label = Label(self, text='???:00 Seconds', bg='LightCyan4', fg='white')
        self.timer_label.place(relx=0.5, rely=0.4, anchor=S)

        self.right_label = Label(self, text=text[next_char:], fg='grey')
        self.right_label.place(relx=0.5, rely=0.5, anchor=W)

        self.middle_label = Label(self, text='', bg='grey')
        self.middle_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.left_label = Label(self, text='', fg='green', bg='wheat3')
        self.left_label.place(relx=0.5, rely=0.5, anchor=E)

        self.current_char = Label(self, text=text[next_char], fg='white', bg='salmon')
        self.current_char.place(relx=0.5, rely=0.6, anchor=N)





        self.bind('<Key>', self.key_pressed)

        #timer logic
        self.after(60000, self.stop_test)
        self.after(1000, self.add_second)

    def add_second(self):
        self.passed_seconds += 1
        try:
            self.timer_label.configure(text=f'???:{self.passed_seconds} Sec', bg='LightCyan4', fg='white')
        except tkinter.TclError:
            pass

        if self.is_typing:
            self.after(1000, self.add_second)

    def stop_test(self):
        self.is_typing = False

        self.words_count = len(self.left_label.cget('text').split(' '))
        self.chars_count = len(self.left_label.cget('text').replace(" ", ""))
        self.accuracy = (self.words_count - self.typo_mistake) * 100 / self.words_count
        #destroy widgets:

        self.right_label.destroy()
        self.left_label.destroy()
        self.current_char.destroy()
        self.middle_label.destroy()
        self.timer_label.destroy()

        #call result function
        self.typing_result()


    def typing_result(self):

        self.wpm_label = Label(self, text=f'???? WPM : {self.words_count}', fg='white', bg='indian red')
        self.wpm_label.place(relx=0.5, rely=0.4, anchor=CENTER)

        self.cpm_label = Label(self, text=f'??? CPM :{self.chars_count}', fg='white', bg='DeepSkyBlue4')
        self.cpm_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.accuracy_label = Label(self, text=f'???? Accuracy : {self.accuracy:.2f}%', fg='white', bg='PaleGreen4')
        self.accuracy_label.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.restart_btn = Button(self, text='???? Restart Test',command=self.restart_app, bg='orange', fg='white')
        self.restart_btn.place(relx=0.5, rely=0.8, anchor=CENTER)


    def restart_app(self):
        self.wpm_label.destroy()
        self.cpm_label.destroy()
        self.restart_btn. destroy()
        self.accuracy_label.destroy()

        self.create_widgets()



    def key_pressed(self, event=None):
        try:
            if event.char == self.right_label.cget('text')[0]:
                self.middle_label.configure(bg='green')
                #move one character from right label
                self.right_label.configure(text=self.right_label.cget('text')[1:])

                #add typed character to left label
                self.left_label.configure(text=self.left_label.cget('text') + event.char)

                if self.right_label.cget('text')[0] ==" ":
                    self.current_char.configure(text="SPACE")
                else:
                    self.current_char.configure(text=self.right_label.cget('text')[0])
                #show character ne to type

            else:
                self.typo_mistake += 1
                self.middle_label.configure(bg="red")
        except tkinter.TclError:
            pass


app = TypingApp()

app.mainloop()
