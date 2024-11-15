import tkinter as tk
from tkinter import ttk
import requests
import json
import time
from auth import post_user_verify, token_login, save_response_to_file, load_and_search
import os
import platform

accesstoken = ""
ACCESSTOKEN = False
api_base_url = "https://stanfordohs.pronto.io/"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Better Pronto")
        self.geometry("600x400")
        self.configure(bg='#2c3e50')
        
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 12), background='#2c3e50', foreground='#ecf0f1')
        self.style.configure('TButton', font=('Helvetica', 10), background='#34495e', foreground='black', padding=10)
        self.style.map('TButton', background=[('active', '#1abc9c')])

        self.label_title = ttk.Label(self, text="Better Pronto", font=("Arial", 24, "bold"))
        self.label_title.pack(pady=20)

        self.label_email = ttk.Label(self, text="Enter @ohs.stanford.edu email:")
        self.label_email.pack(pady=5)
        
        self.entry_email = ttk.Entry(self, font=('Helvetica', 12), width=40)
        self.entry_email.pack(pady=5)

        self.btn_verify = ttk.Button(self, text="Send Verification Email", command=self.send_verification)
        self.btn_verify.pack(pady=10)
        
        self.label_code = ttk.Label(self, text="Enter Verification Code:")
        self.label_code.pack(pady=5)
        
        self.entry_code = ttk.Entry(self, font=('Helvetica', 12), width=40)
        self.entry_code.pack(pady=5)
        
        self.btn_login = ttk.Button(self, text="Login", command=self.login)
        self.btn_login.pack(pady=10)

    def send_verification(self):
        email = self.entry_email.get()
        request_start_time = time.time()
        result = post_user_verify(email)
        request_end_time = time.time()
        total_time = request_end_time - request_start_time
        print(f"Verification email sent: {result}\nRequest took {total_time:.2f} seconds.")

    def login(self):
        email = self.entry_email.get()
        verification_code = self.entry_code.get()

        start_time = time.time()
        logintoken = token_login(email, verification_code)
        end_time = time.time()
        total_time = end_time - start_time
        save_response_to_file(logintoken, 'loginToken.json')
        login_token = load_and_search('loginToken.json', 'logintoken')

        device_info = {
            "browsername": "firefox",
            "browserversion": "130.0.0",
            "osname": "macOS",
            "type": "WEB",
            "uuid": "314c9314-d5e5-4ae4-84e2-9f2f3938ca28",
            "osversion": "10.15.6",
            "appversion": "1.0.0",
        }
        payload = {
            "logintokens": [login_token],
            "device": device_info,
        }
        start_time = time.time()
        response = requests.post(f"{api_base_url}api/v1/user.tokenlogin", json=payload)
        end_time = time.time()
        login_duration = end_time - start_time

        if response.status_code == 200:
            response_data = response.json()
            with open('accessTokenResponse.json', 'w') as file:
                json.dump(response_data, file, indent=4)
            print(f"Login successful\nLogin completed in {login_duration:.2f} seconds. Access Token saved.")
        else:
            response_data = {"error": response.status_code, "message": response.text}
            with open('accessTokenResponse.json', 'w') as file:
                json.dump(response_data, file, indent=4)
            print(f"Error: {response.status_code} - {response.text}")

    def clear_screen(self):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

def checkAccessToken():
    global ACCESSTOKEN, accesstoken
    try:
        with open('accessTokenResponse.json', 'r') as file:
            data = json.load(file)
            accesstoken = data["users"][0]["accesstoken"]
            user_id = data["users"][0]["user"]["id"]
            username = data["users"][0]["user"]["fullname"]
            ACCESSTOKEN = True
    except FileNotFoundError:
        ACCESSTOKEN = False
    if ACCESSTOKEN:
        print(f"Access Token {accesstoken} already exists. Skipping login process.")
        exit()
    else:
        print("Access Token does not exist. Please login to get an access token.")

app = App()
app.mainloop()
