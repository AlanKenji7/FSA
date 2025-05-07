import customtkinter as ctk
from tkinter import *
import sqlite3
from tkinter import messagebox

class BackEnd():
    def conecta_db(self):
       self.conn = sqlite3.connect('FSA BANCO TESTE.db')
       self.cursor= self.conn.cursor()
       print('Banco de dados conectado com sucesso!!')

    def desconecta_db(self):
       self.conn.close()
       print('banco de dados descondctado')

    def criar_tabela(self):
        self.conecta_db()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuarios(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL,
            confirmar_senha TEXT NOT NULL
        );       
""")
        self.conn.commit()
        print('Tabela criada com sucesso!')
        self.desconecta_db()



    def cadastrar_usuario(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirmar_senha_cadastro = self.confirmar_senha_entry.get()

        self.conecta_db()

        self.cursor.execute("""
                INSERT INTO Usuarios (Username,email,senha,confirmar_senha)
                VALUES(?,?,?,?)""", (self.username_cadastro, self.email_cadastro, self.senha_cadastro,
                                    self.confirmar_senha_cadastro))
        
        try:
            
            if (self.username_cadastro == "" or self.email_cadastro == "" or self.senha_cadastro == "" or
                    self.confirmar_senha_cadastro == ""):
                messagebox.showerror(title='Sistema de login', message='ERRO!! por favor\npreencha todos os campos!')
            elif (len(self.username_cadastro) < 4):
                messagebox.showwarning(title='Sistema de login',
                                       message='o nome do usuario deve ser pelo menos de 4 letras')
            elif (len(self.senha_cadastro) < 5):
                messagebox.showwarning(title='Sistema de login', message='A senha deve ter pelo menos 5 caracteres')
            elif (self.senha_cadastro != self.confirmar_senha_cadastro):
                messagebox.showerror(title='Sistema de login', message='ERRO!\nas senhas colocadas são diferentes.')
            else:
                self.conn.commit()
                messagebox.showinfo(title='Sistema de login',
                                    message=f'parabens {self.username_cadastro}\nos dados forma cadastrados com sucesso')
                self.desconecta_db()
                self.limpar_entry_cadastro()
        except sqlite3.Error as e:
            messagebox.showerror(title='Sistema de login',
                                 message=f'ERRO no processamento do seu cadastro\nErro no banco de dados: {e}')
        except Exception as e:
            messagebox.showerror(title='Sistema de login',
                                 message=f'ERRO no processamento do seu cadastro\nPor favor tente novamente: {e}')
        
    def verificar_login(self):
        self.username_login=self.username_login_entry.get()
        self.senha_login=self.senha_login_entry.get()

        self.conecta_db()

        self.cursor.execute("""SELECT * FROM Usuarios WHERE(Username=? AND senha= ?)""",(self.username_login,self.senha_login))
        #mandando selecionar se a senha e o usuario consta noo banco de dados

        self.verfica_dados=self.cursor.fetchall()#procurando na tabela usuarios

        try:
            if(self.username_login in self.verfica_dados and self.senha_login in self.verfica_dados ):
                messagebox.showinfo(title='Sistema de login',message=f'Parabens {self.username_login}\nlogin feito com sucesso')
                self.desconecta_db()
                self.limpa_entry_login()#AQUI EU COLOCO QUE POSSO LIPAR ESSA TELA DEPOIS

        except:
            messagebox.showerror(title='Sistema de login',message='ERRO!\nDados não encontrados no sitema\nverifique os seus dados ou cadastre-se no sistema')
            self.desconecta_db()



class App(ctk.CTk,BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracoes_da_janela_inicial()
        self.mostrar_tela_coepp()
        self.criar_tabela()
        
    #configurando a janela principal
    def configuracoes_da_janela_inicial(self):
        self.geometry("1000x500")
        self.title("FSA Sistema de Login")
        self.resizable(width=False, height=False)#serve para o usuario não ter a liberdade de mexer no tamanho da tela

#comentario
    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_tela_coepp(self):
        self.limpar_tela()
        self.tela_coepp_widgets()

#widgets da tela coepp
    def tela_coepp_widgets(self):
        self.img_coepp = PhotoImage(file='my.app/cooeep.png')
        self.lb_img_coepp = ctk.CTkLabel(self, text=None, image=self.img_coepp)
        self.lb_img_coepp.grid(column=0, row=0, padx=1, pady=1)  # Ajuste o grid para a tela inteira

         # Frame para o botão "Ir ao login"
        self.frame_coeep = ctk.CTkFrame(self, width=350, height=100)  # Reduza a altura do frame
        self.frame_coeep.place(relx=0.8, rely=0.1, anchor='center') # Centralize o frame na parte inferior

        self.btn_ir_ao_login = ctk.CTkButton(self.frame_coeep, width=300, text='Ir ao login'.upper(),
                                             font=('Century Ghotic bold', 18), fg_color='Turquoise',
                                             command=self.mostrar_tela_de_login)
        self.btn_ir_ao_login.pack(padx=10, pady=10) # Use pack para centralizar no frame


    def mostrar_tela_de_login(self):
        self.limpar_tela()
        self.mostrar_tela_de_login_widgets()       

    def mostrar_tela_de_login_widgets(self):
        # configurando as imagens
        self.img_fsa = PhotoImage(file='my.app/img.png.fsa.png')
        self.lb_img_fsa = ctk.CTkLabel(self,text=None, image=self.img_fsa)
        self.lb_img_fsa.grid(column=0, row=1,padx=1)

        #titulo da plataforma
        self.title =ctk.CTkLabel(self,text="Faça o seu login\nou Cadastre-se!",font=('Arial Bold', 23),corner_radius=15)
        self.title.grid(column=1, row=0 ,pady=10, padx=110)

        #frame do formulario de login
        self.frame_login = ctk.CTkFrame(self,width=350,height=410)
        self.frame_login.place(x=620,y=60)

        #colocando widgets dentro do frame de formulario de login
        self.lb_title = ctk.CTkLabel(self.frame_login,text='Faça o seu login',font=('Arial Bold',34))
        self.lb_title.grid(column=0, row=0, padx=10, pady=10)

        self.username_login_entry = ctk.CTkEntry (self.frame_login,width=300,placeholder_text='Digite seu RA',font=('Arial Bold',20),corner_radius=20)
        self.username_login_entry.grid(column=0, row=1, padx=10, pady=10)

        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text='Digite sua senha..',font=('Arial Bold',20),corner_radius=20,border_color='black',show='*')
        self.senha_login_entry.grid(column=0, row=2, padx=10, pady=10)


        self.ver_senha = ctk.CTkCheckBox(self.frame_login,text='Clique para ver a senha',font=('Arial Bold',20),corner_radius = 15,border_color='green')
        self.ver_senha.grid (column=0, row=3, padx=10, pady=10)


        self.btn_login = ctk.CTkButton(self.frame_login, width= 300,text ='Fazer login'.upper(),font=('Arial Bold',20),fg_color='blue',command=self.verificar_login)
        self.btn_login.grid(column=0, row=4, padx=10, pady=10)
    


        self.spam=ctk.CTkLabel(self.frame_login,text='se não tiver uma conta\n cliquem no botão abaixo para poder se cadastrar!',font=('Arial Bold',16))
        self.spam.grid(column=0, row=5, padx=10, pady=10)

        self.btn_cadastro = ctk.CTkButton(self.frame_login, width=300,fg_color="green", text='Cadastre-se'.upper(),font=('Century Ghotic bold', 19),command = self.tela_cadastro)
        self.btn_cadastro.grid(column=0, row=6, padx=10, pady=10)


    def mostrar_tela_cadastro(self):
        self.limpar_tela()
        self.tela_cadastro() 

    def tela_cadastro(self):
            # remover o formulario de login
            self.frame_login.place_forget()

            #frame de formulario de cadastro
            self.frame_cadastro = ctk.CTkFrame(self, width=350, height=410)
            self.frame_cadastro.place(x=620, y=80)

            #criando o nosso titulo
            self.lb_title = ctk.CTkLabel(self.frame_cadastro, text='Faça o seu login', font=('Century Ghotic', 22, 'bold'),corner_radius=15)
            self.lb_title.grid()


            #criando os widgets da tela de cadastro
            self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text='Digite seu nome completo',
            font=('Century Ghotic bold', 16), corner_radius=15, border_color='black')
            self.username_cadastro_entry.grid(column=0, row=1, padx=10, pady=5)

            self.RA_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text='Digite seu RA',
            font=('Century Ghotic bold', 16), corner_radius=15, border_color='black')
            self.RA_cadastro_entry.grid(column=0, row=2, padx=10, pady=5)

            self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro,width=300, placeholder_text='Email do usuario',
            font=('Century Ghotic bold', 16), corner_radius=15,border_color='black')
            self.email_cadastro_entry.grid(column=0, row=3, padx=10, pady=5)

            self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300,placeholder_text='senha do usuario..',
            font=('Century Ghotic bold', 16), corner_radius=20,border_color='black', show='*')
            self.senha_cadastro_entry.grid(column=0, row=4, padx=10, pady=5)

            self.confirmar_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=300,placeholder_text='Confirmar senha..',
            font=('Century Ghotic bold', 16), corner_radius=20,border_color='black', show='*')
            self.confirmar_senha_entry.grid(column=0, row=5, padx=10, pady=5)

            self.ver_senha = ctk.CTkCheckBox(self.frame_cadastro, text='Clique para ver a senha', font=('Century Ghotic bold', 12), corner_radius=15, border_color='green')
            self.ver_senha.grid(column=0, row=6, padx=10, pady=5)


            self.btn_cadastro_user = ctk.CTkButton(self.frame_cadastro, width= 300,text ='Fazer cadastro'.upper(), font=('Century Ghotic bold', 18),fg_color='green',command=self.cadastrar_usuario)
            self.btn_cadastro_user.grid(column=0, row=7, padx=10, pady=5)



            self.btn_login_back = ctk.CTkButton(self.frame_cadastro, width= 300,text ='Voltar ao login'.upper(), font=('Century Ghotic bold', 18),fg_color='Turquoise',command=self.mostrar_tela_de_login_widgets)
            self.btn_login_back.grid(column=0, row=8, padx=10, pady=5)

    def limpar_entry_limpar_cadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)
        self.confirma_senha__entry.delete(0, END)

    def limpa_entry_login(self):
        self.username_login_entry.delete(0, END)
        self.senha_login_entry.delete(0, END)



if __name__ == "__main__":
    app = App()
    app.mainloop()
