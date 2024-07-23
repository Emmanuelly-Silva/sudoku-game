from tkinter import *
from tkinter import font
from tkinter import messagebox
from board import sudoku_board
import random


class Colors:
    def __init__(self):
        self.white = '#FEFFFF'
        self.black = '#000000'
        self.light_sea_green = '#20B2AA'
        self.light_blue = '#D6EAF8'
        self.light_gray = '#58708D'


class Fonts:
    def __init__(self):
        self.notification = font.Font(family="Verdana", size=16, weight='bold')
        self.board_fields = font.Font(family="Calibri", size=19, weight='normal')
        self.btns = font.Font(family="Calibri", size=16, weight='bold')
        self.secundary_font = font.Font(family="Verdana", size=15, weight='bold')


class Sudoku:
    def __init__(self):
        root = Tk()
        self.root = root
        self.color = Colors()
        self.font = Fonts()
        self.num_board = sudoku_board()
        self.entries = []

        self.screen()
        self.create_frames()
        self.create_widgets()
        self.choose_difficulty()
        self.create_board()
        self.game_control()
        
        self.root.mainloop()

    def screen(self):
        self.root.title('Sudoku')
        self.root.geometry('800x650')
        self.root.resizable(False, False)
        self.root.configure(bg=self.color.light_gray)

    def create_frames(self):
        self.header = Frame(self.root, bg=self.color.light_gray, width=800, height=110)
        self.header.pack(pady=10)
        self.header.pack_propagate(False)

        self.notification_frame = Frame(self.header, bg=self.color.light_gray)
        self.notification_frame.pack()

        self.notification_lb = Label(self.notification_frame, bg=self.color.light_gray)
        self.notification_lb.pack()

        self.difficulty_frame = Frame(self.header, bg=self.color.light_gray)

        self.board_frame = Frame(
            self.root, borderwidth=2, bg=self.color.light_gray, highlightbackground=self.color.white, 
            highlightthickness=2, relief=RAISED
        )
        self.board_frame.pack()

        self.btns_frame = Frame(self.root, bg=self.color.light_gray)
        
    def create_widgets(self):
        self.difficulty = StringVar(value='')

        self.easy_difficulty_btn = Radiobutton(
            self.difficulty_frame, text='FÁCIL', variable=self.difficulty,
            value='f', font=self.font.btns, bg=self.color.light_sea_green, width=12, 
            fg=self.color.white, pady=1, selectcolor=self.color.light_sea_green, indicatoron=0,
            activebackground=self.color.light_sea_green, activeforeground=self.color.white, 
            highlightthickness=3, highlightbackground=self.color.black, relief=RAISED, overrelief=RIDGE,
            command=self.start_board
        )

        self.medium_difficulty_btn = Radiobutton(
            self.difficulty_frame, text='NORMAL', variable=self.difficulty,
            value='m', font=self.font.btns, bg=self.color.light_sea_green, width=12,
            fg=self.color.white, pady=1, selectcolor=self.color.light_sea_green, indicatoron=0,
            activebackground=self.color.light_sea_green, activeforeground=self.color.white, 
            highlightthickness=3, highlightbackground=self.color.black, relief=RAISED, overrelief=RIDGE,
            command=self.start_board
        )

        self.hard_difficulty_btn = Radiobutton(
            self.difficulty_frame, text='DIFÍCIL', variable=self.difficulty,
            value='d', font=self.font.btns, bg=self.color.light_sea_green, width=12, 
            fg=self.color.white, pady=1, selectcolor=self.color.light_sea_green, indicatoron=0,
            activebackground=self.color.light_sea_green, activeforeground=self.color.white, 
            highlightthickness=3, highlightbackground=self.color.black, relief=RAISED, overrelief=RIDGE,
            command=self.start_board
        )

    def show_notification(self, txt, **config):
        self.notification_lb['text'] = txt
        self.notification_lb.configure(**config)

    def hide_difficulty(self):
        self.show_notification(
            'Insira um número de 1 a 9 em um campo válido\n\n'
            'Aperte a tecla ENTER para confirmar a jogada!', font=self.font.secundary_font, 
            fg=self.color.white, justify=CENTER
        )
        self.difficulty_frame.pack_forget()

    def show_difficulty(self):
        self.show_notification('ESCOLHA UMA DIFICULDADE', font=self.font.notification, fg=self.color.white)
        self.difficulty.set('')
        self.difficulty_frame.pack()

    def choose_difficulty(self):
        self.difficulty_frame.pack()
        self.show_notification('ESCOLHA UMA DIFICULDADE:', font=self.font.notification, fg=self.color.white)

        self.easy_difficulty_btn.pack(side='left', padx=15, pady=15)
        self.medium_difficulty_btn.pack(side='left', padx=15, pady=15)
        self.hard_difficulty_btn.pack(side='left', padx=15, pady=15)

    def create_board(self):
        for row in range(9):
            entry_row = []
            for col in range(9):
                e = Entry(
                    self.board_frame, font=self.font.board_fields, justify=CENTER,  
                    disabledforeground=self.color.black, width=5, disabledbackground=self.color.light_blue
                )
                e.grid(row=row, column=col, ipady=6)
                e.insert(0, 0)
                e.bind(
                    "<Return>", lambda event, r=row, c=col: self.make_move(event, r, c)
                )
                e['state'] = 'disabled'
                entry_row.append(e)
            self.entries.append(entry_row)

    def fill_board(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col]['state'] = 'normal'
                self.entries[row][col].delete(0, END)
                self.entries[row][col].insert(0, self.num_board[row][col])
                self.entries[row][col]['state'] = 'disabled'

    def set_clues(self):
        if self.difficulty.get() == 'f':
            clues_removed = 35
        elif self.difficulty.get() == 'm':
            clues_removed = 50
        else:
            clues_removed = 55

        for _ in range(clues_removed):
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            while int(self.entries[row][col].get()) == 0:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
            self.entries[row][col]['state'] = 'normal'
            self.entries[row][col].delete(0, END)
            self.entries[row][col].insert(0, 0)
            self.entries[row][col]['state'] = 'disabled'

        for row in range(9):
            for col in range(9):
                if int(self.entries[row][col].get()) == 0:
                    self.entries[row][col]['state'] = 'normal'

    def check_positions(self, row, col, num):
        for i in range(9):
            if i != col and int(self.entries[row][i].get()) == num:
                return False
            if i != row and int(self.entries[i][col].get()) == num:
                return False

        row_block, col_block = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if (row_block + i != row and col_block + j != col
                        and int(self.entries[row_block + i][col_block + j].get()) == num):
                    return False
        return True

    def make_move(self, event, row, col):
        try:
            num = self.entries[row][col].get()
            if not num.isdigit():
                raise ValueError(
                    'Informe uma jogada válida!\n\n'
                    'Número inteiro no intervalo [1, 9]'
                )
            num = int(num)
            if not (1 <= num <= 9):
                raise ValueError(
                    'Informe uma jogada válida!\n\n'
                    'O número deve estar no intervalo [1, 9]'
                )

            if self.check_positions(row, col, num):
                self.entries[row][col].delete(0, END)
                self.entries[row][col].insert(0, num)
                self.entries[row][col]['state'] = 'disabled'
                self.show_notification(
                    'Insira um número de 1 a 9 em um campo válido(0)\n\n'
                    'Aperte a tecla ENTER para confirmar a jogada!', font=self.font.secundary_font, 
                    fg=self.color.white, justify='center'
                )
                if self.check_win():
                    messagebox.showinfo(
                        'Fim de Jogo',
                        'Parabéns, o tabuleiro está completo e você venceu o jogo!!'
                    )

                elif self.check_loss():
                    messagebox.showinfo(
                        'Fim de Jogo',
                        'Você perdeu! Tente novamente com outro tabuleiro!'
                    )
                return True
            else:
                raise ValueError(
                    'Informe uma jogada válida!\n\n'
                    'Número que não esteja presente na mesma linha, coluna ou bloco'
                )
        except ValueError as e:
            self.entries[row][col].delete(0, END)
            self.show_notification(e, font=self.font.secundary_font, fg=self.color.white)
            return False

    def start_board(self):
        self.hide_difficulty()
        self.fill_board()
        self.set_clues()

    def check_win(self):
        for row in self.entries:
            for entry in row:
                if int(entry.get()) == 0:
                    return False
        return True
    
    def check_loss(self):
        for row in range(9):
            for col in range(9):
                if int(self.entries[row][col].get()) == 0:
                    for num in range(1, 10):
                        if self.check_positions(row, col, num):
                            return False
        return True

    def game_control(self):
        self.btns_frame.pack(padx=10, pady=5)

        btn_reset = Button(
            self.btns_frame, text='REINICIAR', font=self.font.btns, 
            bg=self.color.light_sea_green, width=12, fg=self.color.white, pady=1, 
            activebackground=self.color.light_sea_green, activeforeground=self.color.white, 
            highlightthickness=3, highlightbackground=self.color.black, relief=RAISED, overrelief=RIDGE,
            command=self.reset_game
        )
        btn_reset.pack(side='left', padx=30, pady=15)
        btn_quit = Button( 
            self.btns_frame, text='SAIR', font=self.font.btns, bg=self.color.light_sea_green, 
            width=12, fg=self.color.white, pady=1, activebackground=self.color.light_sea_green, 
            activeforeground=self.color.white, highlightthickness=3, highlightbackground=self.color.black,
            relief=RAISED, overrelief=RIDGE, command=self.root.destroy
        )
        btn_quit.pack(side='left', padx=30, pady=15)

    def reset_game(self):
        for row in self.entries:
            for entry in row:
                entry['state'] = 'normal'
                entry.delete(0, END)
                entry.insert(0, 0)
                entry['state'] = 'disabled'
        self.show_difficulty()


Sudoku()
