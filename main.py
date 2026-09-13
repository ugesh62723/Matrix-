import os
import json
from datetime import datetime
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Line

def get_file_path(filename):
    app = App.get_running_app()
    if app:
        return os.path.join(app.user_data_dir, filename)
    return filename

COLOR_PALETTE = {
    "Neon Green": (0, 1, 0.25, 1),
    "Cyan": (0, 1, 1, 1),
    "Electric Blue": (0, 0.5, 1, 1),
    "Hot Pink": (1, 0.08, 0.58, 1),
    "Orange": (1, 0.5, 0, 1),
    "Yellow": (1, 1, 0, 1),
    "White": (1, 1, 1, 1),
    "Red": (1, 0.2, 0.2, 1),
    "Purple": (0.7, 0.2, 1, 1),
    "Gold": (1, 0.84, 0, 1),
    "Magenta": (1, 0, 1, 1),
    "Lime": (0.5, 1, 0, 1),
    "Spring Green": (0, 1, 0.5, 1),
    "Deep Sky Blue": (0, 0.75, 1, 1),
    "Violet": (0.9, 0.5, 1, 1),
    "Coral": (1, 0.5, 0.31, 1),
    "Turquoise": (0.25, 0.88, 0.82, 1),
    "Bright Gold": (1, 0.9, 0.2, 1),
    "Neon Pink": (1, 0.4, 0.8, 1),
    "Bright Teal": (0, 0.9, 0.8, 1),
    "Mint": (0.6, 1, 0.8, 1),
    "Peach": (1, 0.7, 0.6, 1),
    "Lavender": (0.8, 0.6, 1, 1),
    "Electric Yellow": (0.9, 1, 0.2, 1)
}

def calc_fn(x):
    return eval(x, {"__builtins__": {}}, {})

def save_name(name):
    with open(get_file_path("user_name.txt"), "w") as f:
        f.write(name)

def load_name():
    path = get_file_path("user_name.txt")
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().strip()
    return None

def load_history():
    path = get_file_path("history.json")
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history_list):
    with open(get_file_path("history.json"), "w") as f:
        json.dump(history_list, f, indent=2)

def add_to_history(expr, result):
    history_list = load_history()
    now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    history_list.append({"time": now, "calc": f"{expr} = {result}"})
    save_history(history_list)

def save_theme(theme_name):
    with open(get_file_path("theme.json"), "w") as f:
        json.dump({"theme": theme_name}, f)

def load_theme():
    path = get_file_path("theme.json")
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                return data.get("theme", "Neon Green")
        except:
            return "Neon Green"
    return "Neon Green"


class NameEntryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        self.layout.add_widget(Label(size_hint_y=0.2))
        self.lbl_title = Label(
            text="ENTER YOUR NAME", 
            font_size='20sp', 
            bold=True, 
            size_hint_y=0.1
        )
        self.layout.add_widget(self.lbl_title)
        
        self.name_input = TextInput(
            multiline=False, 
            font_size='22sp', 
            halign='center',
            size_hint=(1, None), 
            height='50dp',
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        self.name_input.bind(on_text_validate=self.submit_name)
        self.layout.add_widget(self.name_input)
        
        self.enter_btn = Button(
            text="ENTER", 
            font_size='18sp', 
            bold=True,
            background_normal='',
            color=(0, 0, 0, 1),
            size_hint=(1, None), 
            height='50dp'
        )
        self.enter_btn.bind(on_press=self.submit_name)
        self.layout.add_widget(self.enter_btn)
        
        self.layout.add_widget(Label(size_hint_y=0.4))
        self.add_widget(self.layout)

    def on_enter(self):
        self.apply_theme()

    def apply_theme(self):
        app = App.get_running_app()
        color = app.theme_color
        self.lbl_title.color = color
        self.enter_btn.background_color = color

    def submit_name(self, instance):
        name = self.name_input.text.strip().upper() or "USER"
        save_name(name)
        app = App.get_running_app()
        app.user_name = name
        self.manager.current = 'welcome'


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=dp(2))
        self.lbl_welcome = Label(text="WELCOME", font_size='18sp', color=(1, 1, 1, 1), size_hint_y=None, height=dp(25))
        self.lbl_name = Label(text="", font_size='38sp', bold=True, size_hint_y=None, height=dp(50))
        
        self.layout.add_widget(Label(size_hint_y=0.4))
        self.layout.add_widget(self.lbl_welcome)
        self.layout.add_widget(self.lbl_name)
        self.layout.add_widget(Label(size_hint_y=0.6))
        self.add_widget(self.layout)

    def on_enter(self):
        app = App.get_running_app()
        self.lbl_name.color = app.theme_color
        if app.saved_flag:
            self.lbl_welcome.text = "WELCOME BACK"
        else:
            self.lbl_welcome.text = "WELCOME"
        self.lbl_name.text = app.user_name
        Clock.schedule_once(self.go_to_calc, 1.2)

    def go_to_calc(self, dt):
        self.manager.current = 'calculator'


class CalculatorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expression = ""
        
        self.main_layout = BoxLayout(orientation='vertical', padding=[dp(10), dp(0), dp(10), dp(10)], spacing=dp(4))
        
        top_bar = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(2))
        
        self.top_label = Label(
            text="> CREATED BY YUVRAJ SHARMA_", 
            font_size='16sp', 
            bold=True, 
            halign='left',
            valign='middle'
        )
        self.top_label.bind(size=lambda s, w: setattr(s, 'text_size', (s.width, s.height)))
        top_bar.add_widget(self.top_label)
        
        self.theme_btn = Button(
            text="THEME", 
            font_size='9sp', 
            bold=True,
            background_normal='',
            background_color=(0.1, 0.1, 0.2, 1),
            size_hint_x=0.18
        )
        self.theme_btn.bind(on_press=self.open_theme_popup)
        top_bar.add_widget(self.theme_btn)

        self.hist_btn = Button(
            text="HISTORY", 
            font_size='9sp', 
            bold=True,
            background_normal='',
            background_color=(0, 0.13, 0, 1),
            size_hint_x=0.18
        )
        self.hist_btn.bind(on_press=self.open_history)
        top_bar.add_widget(self.hist_btn)

        self.logout_btn = Button(
            text="LOG OUT", 
            font_size='9sp', 
            bold=True,
            background_normal='',
            background_color=(0.13, 0.13, 0.13, 1),
            color=(1, 0.4, 1, 1),
            size_hint_x=0.18
        )
        self.logout_btn.bind(on_press=self.logout)
        top_bar.add_widget(self.logout_btn)

        self.main_layout.add_widget(top_bar)
        self.main_layout.add_widget(Label(size_hint_y=1))

        user_bar = BoxLayout(size_hint_y=None, height=dp(22))
        self.user_label = Label(
            text="USER: ", 
            font_size='13sp', 
            bold=True,
            color=(0.5, 0.5, 0.5, 1), 
            halign='left', 
            valign='middle'
        )
        self.user_label.bind(size=lambda s, w: setattr(s, 'text_size', (s.width, s.height)))
        user_bar.add_widget(self.user_label)
        self.main_layout.add_widget(user_bar)

        display_box = BoxLayout(orientation='vertical', padding=dp(8), size_hint_y=None, height=dp(95))
        with display_box.canvas.before:
            self.border_color = Color(0, 1, 0.25, 1)
            self.border_rect = Line(rectangle=(0, 0, 0, 0), width=1)

        def update_border(*args):
            self.border_rect.rectangle = (display_box.x, display_box.y, display_box.width, display_box.height)

        display_box.bind(pos=update_border, size=update_border)

        self.lbl_input = Label(
            text="", 
            font_size='28sp', 
            bold=True, 
            halign='right', 
            valign='middle'
        )
        self.lbl_input.bind(size=self.lbl_input.setter('text_size'))
        
        self.lbl_live = Label(
            text="", 
            font_size='18sp', 
            color=(0.6, 0.6, 0.6, 1), 
            halign='right', 
            valign='middle'
        )
        self.lbl_live.bind(size=self.lbl_live.setter('text_size'))
        
        display_box.add_widget(self.lbl_input)
        display_box.add_widget(self.lbl_live)
        self.main_layout.add_widget(display_box)

        self.grid = GridLayout(cols=4, spacing=dp(2), size_hint_y=None, height=dp(300))
        buttons = [
            ('7', 0.08, 0.08, 0.08), ('8', 0.08, 0.08, 0.08), ('9', 0.08, 0.08, 0.08), ('/', 0, 0, 0),
            ('4', 0.08, 0.08, 0.08), ('5', 0.08, 0.08, 0.08), ('6', 0.08, 0.08, 0.08), ('*', 0, 0, 0),
            ('1', 0.08, 0.08, 0.08), ('2', 0.08, 0.08, 0.08), ('3', 0.08, 0.08, 0.08), ('-', 0, 0, 0),
            ('.', 0.08, 0.08, 0.08), ('0', 0.08, 0.08, 0.08), ('+', 0, 0, 0), ('=', 0, 0, 0)
        ]
        
        self.grid_buttons = []
        for text, r, g, b in buttons:
            btn = Button(
                text=text, 
                font_size='20sp', 
                bold=True,
                background_normal='',
                background_color=(r, g, b, 1)
            )
            btn.bind(on_press=self.on_btn_click)
            self.grid.add_widget(btn)
            self.grid_buttons.append(btn)
            
        self.main_layout.add_widget(self.grid)

        bottom_bar = BoxLayout(spacing=dp(6), size_hint_y=None, height=dp(50))
        ac_btn = Button(
            text="AC", 
            font_size='16sp', 
            bold=True,
            background_normal='',
            background_color=(0.2, 0, 0, 1),
            color=(1, 0.23, 0.23, 1)
        )
        ac_btn.bind(on_press=self.btn_all_clear)
        
        self.del_btn = Button(
            text="DEL", 
            font_size='16sp', 
            bold=True,
            background_normal='',
            background_color=(0.13, 0.13, 0.13, 1)
        )
        self.del_btn.bind(on_press=self.btn_del)
        
        bottom_bar.add_widget(ac_btn)
        bottom_bar.add_widget(self.del_btn)
        self.main_layout.add_widget(bottom_bar)

        self.add_widget(self.main_layout)

    def on_enter(self):
        app = App.get_running_app()
        self.user_label.text = f"USER: {app.user_name}"
        self.apply_theme()

    def apply_theme(self):
        app = App.get_running_app()
        c = app.theme_color
        dark_op_bg = (c[0]*0.25, c[1]*0.25, c[2]*0.25, 1)

        self.top_label.color = c
        self.theme_btn.color = c
        self.hist_btn.color = c
        self.lbl_input.color = c
        self.del_btn.color = c
        self.border_color.rgba = c

        for btn in self.grid_buttons:
            if btn.text == '=':
                btn.background_color = c
                btn.color = (0, 0, 0, 1)
            elif btn.text in ['/', '*', '-', '+']:
                btn.background_color = dark_op_bg
                btn.color = c
            else:
                btn.color = c

    def open_theme_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=2, spacing=dp(8), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        popup = Popup(
            title="SELECT THEME COLOR (24)",
            content=content,
            size_hint=(0.9, 0.8),
            auto_dismiss=True
        )

        for theme_name, rgba in COLOR_PALETTE.items():
            btn = Button(
                text=theme_name,
                font_size='12sp',
                bold=True,
                size_hint_y=None,
                height=dp(45),
                background_normal='',
                background_color=(0.15, 0.15, 0.15, 1),
                color=rgba
            )
            btn.bind(on_press=lambda b, name=theme_name: self.change_theme(name, popup))
            grid.add_widget(btn)

        scroll.add_widget(grid)
        content.add_widget(scroll)
        popup.open()

    def change_theme(self, theme_name, popup):
        app = App.get_running_app()
        app.set_theme(theme_name)
        self.apply_theme()
        popup.dismiss()

    def update_live_answer(self):
        try:
            if not self.expression:
                self.lbl_live.text = ""
                return
            temp = self.expression
            while temp and temp[-1] in ['+', '-', '*', '/', '.']:
                temp = temp[:-1]
            if not temp:
                self.lbl_live.text = ""
                return
            res = str(calc_fn(temp))
            self.lbl_live.text = "= " + res
        except:
            self.lbl_live.text = ""

    def on_btn_click(self, instance):
        item = instance.text
        if item == '=':
            self.btn_equal()
            return
            
        if self.expression and self.expression[-1] in ['+', '-', '*', '/', '.'] and item in ['+', '-', '*', '/', '.']:
            if item == self.expression[-1]:
                return
            self.expression = self.expression[:-1] + str(item)
        else:
            self.expression += str(item)
            
        self.lbl_input.text = self.expression
        self.update_live_answer()

    def btn_all_clear(self, instance=None):
        self.expression = ""
        self.lbl_input.text = ""
        self.lbl_live.text = ""

    def btn_del(self, instance=None):
        self.expression = self.expression[:-1]
        self.lbl_input.text = self.expression
        self.update_live_answer()

    def btn_equal(self):
        try:
            temp = self.expression
            while temp and temp[-1] in ['+', '-', '*', '/', '.']:
                temp = temp[:-1]
            result = str(calc_fn(temp))
            add_to_history(temp, result)
            self.lbl_input.text = result
            self.lbl_live.text = ""
            self.expression = result
        except:
            self.lbl_input.text = "Error"
            self.lbl_live.text = ""
            self.expression = ""

    def open_history(self, instance):
        self.manager.current = 'history'

    def logout(self, instance=None):
        path = get_file_path("user_name.txt")
        if os.path.exists(path):
            os.remove(path)
        app = App.get_running_app()
        app.user_name = ""
        app.saved_flag = False
        self.btn_all_clear()
        self.manager.current = 'name_entry'


class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        self.add_widget(self.main_layout)

    def on_enter(self):
        self.main_layout.clear_widgets()
        app = App.get_running_app()
        c = app.theme_color
        history_list = load_history()

        self.main_layout.add_widget(Label(
            text="> CALCULATION HISTORY_", 
            font_size='14sp', 
            bold=True, 
            color=c,
            size_hint_y=None, 
            height='30dp'
        ))
        
        self.main_layout.add_widget(Label(
            text=f"[ USER: {app.user_name} ] [ TOTAL: {len(history_list)} LOGS ]", 
            font_size='10sp', 
            color=(0.4, 0.4, 0.4, 1),
            size_hint_y=None, 
            height='20dp'
        ))

        scroll = ScrollView(size_hint=(1, 1))
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        content.bind(minimum_height=content.setter('height'))

        if not history_list:
            lbl = Label(
                text="\n[!] NO HISTORY FOUND...\n", 
                font_size='12sp', 
                bold=True, 
                color=c,
                size_hint_y=None, 
                height='40dp'
            )
            content.add_widget(lbl)
        else:
            for i, item in enumerate(reversed(history_list), 1):
                txt = f"[{i}] {item['time']}\n    └─> {item['calc']}"
                lbl = Label(
                    text=txt, 
                    font_size='12sp', 
                    bold=True, 
                    color=c,
                    size_hint_y=None, 
                    height='50dp',
                    halign='left',
                    valign='middle'
                )
                lbl.bind(size=lbl.setter('text_size'))
                content.add_widget(lbl)

        scroll.add_widget(content)
        self.main_layout.add_widget(scroll)

        btn_bar = BoxLayout(spacing=5, size_hint_y=None, height='45dp')
        
        back_btn = Button(
            text="< BACK", 
            font_size='11sp', 
            bold=True,
            background_normal='',
            background_color=(0.1, 0.1, 0.1, 1),
            color=(1, 1, 1, 1)
        )
        back_btn.bind(on_press=self.go_back)
        
        logout_btn = Button(
            text="LOG OUT", 
            font_size='11sp', 
            bold=True,
            background_normal='',
            background_color=(0.26, 0, 0.26, 1),
            color=(1, 0.4, 1, 1)
        )
        logout_btn.bind(on_press=self.logout)
        
        clear_btn = Button(
            text="CLEAR DATA", 
            font_size='11sp', 
            bold=True,
            background_normal='',
            background_color=(0.2, 0, 0, 1),
            color=(1, 0.23, 0.23, 1)
        )
        clear_btn.bind(on_press=self.clear_history)

        btn_bar.add_widget(back_btn)
        btn_bar.add_widget(logout_btn)
        btn_bar.add_widget(clear_btn)
        self.main_layout.add_widget(btn_bar)

    def go_back(self, instance):
        self.manager.current = 'calculator'

    def logout(self, instance):
        calc_screen = self.manager.get_screen('calculator')
        calc_screen.logout()

    def clear_history(self, instance):
        path = get_file_path("history.json")
        if os.path.exists(path):
            os.remove(path)
        self.on_enter()


class CalculatorApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        self.title = "Matrix"
        self.user_name = ""
        self.saved_flag = False
        
        self.current_theme = load_theme()
        self.theme_color = COLOR_PALETTE.get(self.current_theme, (0, 1, 0.25, 1))

        sm = ScreenManager()
        sm.add_widget(NameEntryScreen(name='name_entry'))
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(CalculatorScreen(name='calculator'))
        sm.add_widget(HistoryScreen(name='history'))

        saved = load_name()
        if saved:
            self.user_name = saved
            self.saved_flag = True
            sm.current = 'welcome'
        else:
            sm.current = 'name_entry'

        return sm

    def set_theme(self, theme_name):
        if theme_name in COLOR_PALETTE:
            self.current_theme = theme_name
            self.theme_color = COLOR_PALETTE[theme_name]
            save_theme(theme_name)

if __name__ == '__main__':
    CalculatorApp().run()
            
