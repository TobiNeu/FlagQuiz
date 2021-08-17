from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import random

class FlaggenQuiz(App):
    def build(self):
        ### Window setup
        Window.clearcolor = (64/255,64/255,64/255,1)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.7,0.8)
        self.window.pos_hint = {'center_x':0.5, 'center_y':0.5}

        #add widgets to start window
        self.image = Image(source = 'start_image.png')
        self.window.add_widget(self.image)

        self.text = Label(text='Herzlich Willkommen zum Flaggen-Quiz!',
                          font_size = 18,
                          bold = True,
                          halign = 'center',
                          valign = 'center')
        self.window.add_widget(self.text)

        self.startbutton = Button(text='Starte Quiz',
                             size_hint=(1,0.5),
                             bold = True,
                             font_size = 16,
                             background_color = (0/255,255/255,255/255))
        self.startbutton.bind(on_press=self.buildquizenvironment)
        self.window.add_widget(self.startbutton)
        Window.bind(on_key_down=self.keypress)
        return self.window

    def buildquizenvironment(self,event):
        ### build quiz layout
        ### create quiz dict
        self.flagdic = self.makedic()

        self.text.text = 'Welches Land ist das? (noch %s Länder)' %(len(self.flagdic))

        self.window.remove_widget(self.startbutton)
        self.input = TextInput(multiline = False,
                               size_hint = (1,0.25))
        self.window.add_widget(self.input)

        self.bottom_grid = GridLayout()
        self.bottom_grid.cols = 3
        self.button = Button(text='Absenden (STRG + A)',
                             size_hint = (1,0.5),
                             bold = True,
                             background_color = (0/255,255/255,255/255))
        self.button.bind(on_press=self.presssubmit)

        self.bottom_grid.add_widget(self.button)
        self.buttonhelp = Button(text='Hilfe (STRG + H)',
                                 size_hint = (1,0.5),
                                 bold = True,
                                 color = (0,0,0))
        self.buttonhelp.bind(on_press=self.showhelp)
        self.bottom_grid.add_widget(self.buttonhelp)

        self.skip = Button(text='Weiter (STRG + W)',
                           size_hint=(1, 0.5),
                           bold=True,
                           color = (0,0,0))

        self.skip.bind(on_press=self.skipquestion)
        self.bottom_grid.add_widget(self.skip)

        self.answercheck = Label(text='',
                                 halign='center',
                                 valign='center'
                                 )
        self.bottom_grid.add_widget(self.answercheck)
        self.helptext = Label(text='',
                              halign='center',
                              valign='center'
                              )
        self.bottom_grid.add_widget(self.helptext)
        self.window.add_widget(self.bottom_grid)
        self.makequestion()

    def makedic(self):
        flagdic = {}
        file = open('flagdic.csv', 'r').readlines()

        for line in file[1:]:
            _,abb, country = line.split(';')
            if not _:
                flagdic[str(abb).lower()] = country

        return flagdic

    def makequestion(self):
        self.abb, self.country = random.choice(list(self.flagdic.items()))
        try:
            self.image.source = 'flag_images/%s.png' % (self.abb)
        except:
            del self.flagdic[self.abb]
            self.makequestion()

    def presssubmit(self,event):
        if str(self.input.text).lower().strip() == str(self.country).lower().strip():
            self.answercheck.text = 'richtig'
            self.helptext.text = ''
            del self.flagdic[self.abb]
            if len(self.flagdic) == 0:
                self.window.remove_widget(self.bottom_grid)
                self.image.source = 'start_image.png'
                self.text.text = 'Herzlichen Glückwunsch, Du hast alle Länderflaggen erkannt!\nBis zum nächsten Mal...'
                self.window.remove_widget(self.input)

            else:
                self.makequestion()
                self.input.text = ''
                self.text.text = 'Welches Land ist das? (noch %s Länder)' % (len(self.flagdic))
        else:
            self.answercheck.text = 'falsch'

    def showhelp(self,event):
        self.helptext.text = self.country
        self.answercheck.text = ''

    def skipquestion(self,event):
        self.makequestion()
        self.answercheck.text = ''
        self.helptext.text = ''

    def keypress(self,*args):
        if 'ctrl' in list(args)[-1] and list(args)[-2] == 'a':
            self.presssubmit(None)
        elif 'ctrl' in list(args)[-1] and list(args)[-2] == 'w':
            self.skipquestion(None)
        elif 'ctrl' in list(args)[-1] and list(args)[-2] == 'h':
            self.showhelp(None)

if __name__ == "__main__":
    FlaggenQuiz().run()