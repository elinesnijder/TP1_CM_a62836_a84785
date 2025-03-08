import flet as ft
from sympy import sympify, N


class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=2):
        super().__init__(            
            text=text,
            on_click=button_clicked,
            expand=expand,
            height=70,  
            width=70,   
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))) 
        self.data = text 


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.GREY
        self.color = ft.colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.TEAL_ACCENT_700
        self.color = ft.colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK


class CalculatorApp(ft.Container):
    # application's root control (i.e. "view") containing all other controls
    def __init__(self):
        super().__init__()
        self.reset()
        self.result = ft.Text(value="0", color=ft.colors.BLACK, size=75)
        self.width = "100%"
        self.height = "100%"
        self.bgcolor = ft.colors.GREY_50
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.alignment = ft.alignment.center
        self.expression = ""
        
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ExtraActionButton(text="AC", button_clicked=self.button_clicked),
                        ExtraActionButton(text="+/-", button_clicked=self.button_clicked),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="0", expand=2, button_clicked=self.button_clicked),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand == True:
                self.result.value = data
                self.expression = data
                self.new_operand = False
            else:
                self.result.value += data
                self.expression += data

        elif data in ("+", "-", "*", "/", "(", ")"):
            self.result.value += data
            self.expression += data
            self.new_operand = False

        elif data == "=":
            try:
                self.result.value = str(N(sympify(self.expression)))
            except:
                self.result.value = "Error"
            self.reset()

        elif data == "%":
            try:
                self.result.value = str(N(sympify(self.expression) / 100))
            except:
                self.result.value = "Error"
            self.reset()

        elif data == "+/-":
            try:
                self.result.value = str(N(-sympify(self.result.value)))
                self.expression = self.result.value
            except:
                self.result.value = "Error"

        self.update()


    def reset(self):
        self.expression = ""
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Calc App"
    page.window_resizable = False
    page.window_width = 400  # Ajustando largura para iOS
    page.window_height = 600  # Ajustando altura para iOS
    page.padding = 0
    page.spacing = 0
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    # create application instance
    calc = CalculatorApp()

    # add application's root control to the page
    page.add(calc)


ft.app(target=main)