"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config

import reflex as rx

button_style = {
    "color": "white",
    "_hover": {"color": "rgb(107,99,246)", "text_decoration": "none"},
}

class User(rx.Model, table=True):
    username: str
    email: str
    password: str 


class State(rx.State):
    input_password: str = ""
    input_password_again: str = ""
    input_mail: str = ""
    input_user: str = ""
    login_state: bool = False
    show_log: bool = False
    show_reg: bool = False
    log_usr_err: bool = False
    log_pw_err: bool = False
    reg_usr_err: bool = False
    reg_pw_err: bool =False

    def show_login(self):
        self.show_log = not (self.show_log)
    def show_register(self):
        self.show_reg = not (self.show_reg)
    
    def login(self):
        print("login")

        self.log_usr_err = False
        self.log_pw_err = False
        yield

        #check if user exists
        with rx.session() as session:
            users = session.query(User).all()
        
        #improvement: list comprehension?
        for i in users:
            print('i.username: ',i.username)
            print('self.input_user: ',self.input_user)
            if self.input_user == i.username:
                print('User exists')
                #compare user pw
                if self.input_password == i.password:
                    print('Password correct.')
                    self.login_state = True
                    self.show_log = False
                    return
                else:
                    print('Password is wrong.')
                    self.log_pw_err = True
                    return
        
        #no user found in user list
        self.log_usr_err = True
        return


    def register(self):
        print("register")

        self.reg_usr_err = False
        self.reg_pw_err = False

        #check if user exists
        with rx.session() as session:
            users = session.query(User).all()

        #improvement: list comprehension?
        for i in users:
            print('i.username: ',i.username)
            print('self.input_user: ',self.input_user)
            if self.input_user == i.username:
                print('User already exists')
                #error that user already exists
                self.reg_usr_err = True
                return
            
        #if user does not exists yet, check pw's
        if self.input_password != self.input_password_again:
            print('Passwords dont match.')
            self.reg_pw_err = True
            return
        
        #if everything is alright, add user to database
        with rx.session() as session:
            session.add(User(username=self.input_user, email=self.input_mail, password=self.input_password))
            session.commit()
        print('User added')
        


    def write_db(self):
        with rx.session() as session:
            session.add(
                User(
                    username="test",
                    email="test@admin.de",
                    password="123",
                )
            )
            session.commit()
    
    def read_db(self):
        with rx.session() as session:
            users = session.query(User).all()
        print(users)

    pass



def navbar_login():
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.link(rx.image(src="/logo.png",width='150px'),href="/"),
                rx.heading("Virtual Stock Portfolio",color="white"),
            ),
            rx.flex(
            rx.button(rx.icon(tag="lock"), on_click=State.show_login),
            rx.modal(rx.modal_overlay(rx.modal_content(
                                rx.modal_header(rx.flex("Login",rx.spacer(),rx.button(rx.icon(tag="small_close"), on_click=State.show_login))),
                                rx.modal_body("sign in with your credentials or create a new account"),
                                rx.modal_body(rx.input(placeholder="username",value=State.input_user,on_change=State.set_input_user)),
                                rx.modal_body(rx.password(placeholder="password",value=State.input_password,on_change=State.set_input_password)),
                                rx.cond(State.log_usr_err,rx.modal_body("username was not found! Please register first.")),
                                rx.cond(State.log_pw_err,rx.modal_body("password was incorrect! Try again.")),
                                rx.modal_footer(rx.button("Login",on_click=State.login)),
                                )),is_open=State.show_log,),
            rx.spacer(),
            rx.button(rx.icon(tag="add"), on_click=State.show_register),
            rx.modal(rx.modal_overlay(rx.modal_content(
                                rx.modal_header(rx.flex("Register",rx.spacer(),rx.button(rx.icon(tag="small_close"), on_click=State.show_register))),
                                rx.modal_body("create a new account"),
                                rx.modal_body(rx.input(placeholder="username",value=State.input_user,on_change=State.set_input_user)),
                                rx.modal_body(rx.input(placeholder="email",value=State.input_mail,on_change=State.set_input_mail)),
                                rx.modal_body(rx.password(placeholder="password",value=State.input_password,on_change=State.set_input_password)),
                                rx.modal_body(rx.password(placeholder="password",value=State.input_password_again,on_change=State.set_input_password_again)),
                                rx.cond(State.reg_usr_err,rx.modal_body("username already exists and cannot be registered! Please log in.")),
                                rx.cond(State.reg_pw_err,rx.modal_body("passwords dont match! Check for typos.")),
                                rx.modal_footer(rx.button("register",on_click=State.register)),
                                )),is_open=State.show_reg,),
           
            rx.button(
                rx.icon(tag="moon"),
                on_click=rx.toggle_color_mode,

            ),width="7%"),
            justify="space-between",
            border_bottom="0.08em solid #F0F0F0",
            padding_x="2em",
            padding_y="1em",
            bg="rgba(43,56,65, 0.97)",
        ),
        position="fixed",
        width="100%",
        top="0px",
        z_index="500", 
    )

def navbar_logout():
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.link(rx.image(src="/logo.png",width='150px'),href="/"),
                rx.heading("Virtual Stock Portfolio",color="white"),
            ),
            rx.flex(
            rx.menu(rx.menu_button("Menu", **button_style),rx.menu_list(rx.menu_item(rx.link(rx.text("Main Page"),href="/")),rx.menu_divider(),rx.menu_item(rx.link(rx.text("Known Issues"),href="/issues")),rx.menu_item(rx.link(rx.text("Help"),href="/help")))),
            rx.spacer(),
            rx.button(
                rx.icon(tag="moon"),
                on_click=rx.toggle_color_mode,

            ),width="7%"),
            justify="space-between",
            border_bottom="0.08em solid #F0F0F0",
            padding_x="2em",
            padding_y="1em",
            bg="rgba(43,56,65, 0.97)",
        ),
        position="fixed",
        width="100%",
        top="0px",
        z_index="500", 
    )


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            navbar_login(),
            rx.cond(State.login_state,
                    rx.text("You are logged in as ",State.input_user)),
            rx.cond(State.login_state,rx.link(rx.button("Open Portfolio"),href='\main')),
        ),
        padding_top="10%")


def main() -> rx.Component:
    return rx.center(
        rx.vstack(
            navbar_logout(),
            rx.text("main portfolio page"),
            spacing="1.5em",
            font_size="1em",
        ),
        padding_top="10%",
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.add_page(main)
app.compile()
