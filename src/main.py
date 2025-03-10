import flet as ft
import math
import re
from datetime import datetime

class HistoryEntry(ft.Row):
    def __init__(self, index, expression, result, delete_callback, copy_callback):
        super().__init__()
        self.controls = [
            ft.Text(f"{index}.", size=10, color=ft.colors.GREY),
            ft.Text(datetime.now().strftime("On %Y-%m-%d, at %H:%M:%S"), size=10, color=ft.colors.GREY),
            ft.Text(f"{expression} = {result}", size=10, color=ft.colors.GREY),
            ft.IconButton(icon=ft.icons.DELETE, on_click=delete_callback),
            ft.IconButton(icon=ft.icons.CONTENT_COPY, on_click=lambda e: copy_callback(result))
        ]
        
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
        self.expression_text = ft.Text(value="", color=ft.colors.GREY, size=25) #campo em cima
       
        self.history = [] #armazenamento do histórico
        self.history_list = ft.ListView(controls=[], expand=True)
        self.index_counter = 1
        self.history_container = ft.Container(
            content=self.history_list,
            height=200,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            visible=False  # Escondido inicialmente
        )
        
        self.width = "100%"
        self.height = "100%"
        self.bgcolor = ft.colors.GREY_50
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.alignment = ft.alignment.center
        self.expression = ""
        self.last_result = None
        self.show_extra_buttons = False #botoes extras
        
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.expression_text], alignment="end"),
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ActionButton(text="√", button_clicked=self.button_clicked),
                        ActionButton(text="^", button_clicked=self.button_clicked),  
                        ActionButton(text="log", button_clicked=self.button_clicked),  
                        ActionButton(text="exp", button_clicked=self.button_clicked),
                        ActionButton(text="!", button_clicked=self.button_clicked),
                        ActionButton(text="|x|", button_clicked=self.button_clicked),
                    ],
                    visible=self.show_extra_buttons
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(text="AC", button_clicked=self.button_clicked),
                        ExtraActionButton(text="CE", button_clicked=self.button_clicked),  
                        ExtraActionButton(text="←", button_clicked=self.button_clicked),  
                        ExtraActionButton(text="↑", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(text="(", button_clicked=self.button_clicked),  
                        ExtraActionButton(text=")", button_clicked=self.button_clicked),  
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
                self.history_container,
                #row de botoes extra
                ft.Row(
                    controls=[ft.IconButton(icon=ft.icons.HISTORY, on_click=self.toggle_history)],
                    alignment="center" 
                ),
            ],
            scroll="adaptive", 
            expand=True,
        )

    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data == "CE":  #apaga o que foi inserido
            self.result.value = "0"
        
        elif data == "←":  
            if self.result.value and self.result.value != "0":
                self.result.value = self.result.value[:-1] #elimina ultimo caractere
                self.expression = self.expression[:-1]  #elimina da expressão
                if not self.result.value:
                    self.result.value = "0"
        
        elif data == "↑": 
            self.show_extra_buttons = not self.show_extra_buttons
            self.content.controls[2].visible = self.show_extra_buttons
            self.update()
                    
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.last_result is not None:  # Se houver um resultado anterior
                self.result.value = data  # Reinicia com o novo número
                self.expression = data
                self.last_result = None  
            elif self.result.value == "0" or self.new_operand:
                self.result.value = data
                self.expression = data
                self.new_operand = False
            else:
                self.result.value += data
                self.expression += data
            self.result.value = self.format_number(self.expression)

        elif data in ("+", "-", "*", "/", "(", ")"):
            #ultimo caractere é operando ou ()
            if self.expression and self.expression[-1] in ("+", "-", "*", "/"):
                #se for, não permite adicionar mais
                #muda de operando se clicar noutro
                if data in ("+", "-", "*", "/"):
                    self.expression = self.expression[:-1] + data
                    self.result.value = self.format_number(self.expression)
                    self.update_expression_display()
                return
            
            # último caractere é um parêntese de abertura
            if self.expression and self.expression[-1] == "(" and data == "(":
                return  #nao adiciona parênteses de abertura consecutivos

            # último caractere é um parêntese de fechamento
            if self.expression and self.expression[-1] == ")" and data == ")":
                return  #nao adiciona parênteses de fechamento consecutivos
            
            if self.last_result is not None:
                self.expression = self.result.value.replace(" ", "")
                self.last_result = None 
            self.result.value += data
            self.expression += data
            self.result.value = self.format_number(self.expression)
            self.new_operand = False
            
        elif data == "=":
            try:
                result = eval(self.expression.replace(" ", ""))
                self.result.value = self.format_number(str(round(result, 2)))
                self.last_result = result
                self.add_to_history(self.expression_text.value, self.result.value)
            except:
                self.result.value = "Error"
                self.last_result = None
            self.update_expression_display()

        elif data == "%":
            try:
                result = eval(self.expression.replace(" ", "")) / 100
                self.result.value = self.format_number(str(round(result, 2)))
            except:
                self.result.value = "Error"
            self.update_expression_display()

        elif data == "+/-":
            try:
                result = -float(self.result.value.replace(" ", ""))
                self.result.value = self.format_number(str(round(result, 2))) #arredondamento
                self.expression = self.result.value
            except:
                self.result.value = "Error"
                
        elif data == "√":
            try:
                result = math.sqrt(float(self.result.value.replace(" ", "")))
                self.result.value = self.format_number(str(round(result, 2)))
            except:
                self.result.value = "Error"
        
        elif data == "^":
            self.expression += "^"
            self.result.value = self.format_number(self.expression)
            
        elif data == "log":
            try:
                result = math.log10(float(self.result.value.replace(" ", "")))
                self.result.value = self.format_number(str(round(result, 2)))
            except:
                self.result.value = "Error"
        
        elif data == "exp":
            try:
                result = math.exp(float(self.result.value.replace(" ", "")))
                self.result.value = self.format_number(str(round(result, 2)))
            except:
                self.result.value = "Error"
                
        elif data == "!":
            try:
                num = int(self.result.value.replace(" ", ""))
                result = math.factorial(num)
                self.result.value = self.format_number(str(result))
            except:
                self.result.value = "Error"
                
        elif data == "|x|":
            try:
                result = abs(float(self.result.value.replace(" ", "")))
                self.result.value = self.format_number(str(round(result, 2)))
            except:
                self.result.value = "Error"
        self.update()

        self.update_expression_display()
    
    def toggle_history(self, e):
        self.history_container.visible = not self.history_container.visible
        self.update()   
         
    def add_to_history(self, expression, result):
            if len(self.history_list.controls) >= 10:
                self.history_list.controls.pop(0)
            entry = HistoryEntry(
                self.index_counter, expression, result,
                lambda e: self.delete_history_entry(entry),
                self.copy_to_clipboard
            )
            self.history_list.controls.insert(0,entry) #altera a ordem para o mais recente estar primeiro
            self.index_counter += 1
            self.update()

    def delete_history_entry(self, entry):
        self.history_list.controls.remove(entry)
        self.update()

    def copy_to_clipboard(self, text):
        self.page.set_clipboard(text)
        print(f"Copiado para área de transferência: {text}")

    def saving_history(self):
        history_data = [entry.value for entry in self.history_list.controls]
        self.page.client_storage.set("calc_history", history_data)
    
    def load_history(self):
        storage_history = self.page.client_storage.get("calc_history")
        if storage_history:
            for index, entry in enumerate(storage_history, start=1):
                self.add_to_history(entry, save=False)

    def format_number(self, number_str):
        try:
            #remover espaços para nao haver erro
            number_str = number_str.replace(" ", "")

            #encontrar os numeros na expressao
            def format_match(match):
                num = match.group()
                if "." in num:  #numeros deciamsi
                    int_part, decimal_part = num.split(".")
                    formatted_int = f"{int(int_part):,}".replace(",", " ")
                    return f"{formatted_int}.{decimal_part}"
                else:  #numeros inteiros
                    return f"{int(num):,}".replace(",", " ")

            #formatação nos numeors todos
            formatted_expression = re.sub(r"-?\d+\.?\d*", format_match, number_str)
            return formatted_expression
        except ValueError:
            return number_str

    def update_expression_display(self):
        self.expression_text.value = self.format_number(self.expression)
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
    page.scroll = "adaptive"
    # create application instance
    calc = CalculatorApp()
    
    scroll_container = ft.Container(
        content=calc, 
        expand=True,
    )
    # add application's root control to the page
    page.add(scroll_container)


ft.app(target=main) 