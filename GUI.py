import requests
import logging
import time
import json
from dataclasses import dataclass, asdict
import tkinter as tk
from tkinter import font

# Custom exception for backend errors
class BackendError(Exception):
    pass

# Dataclass for device information
@dataclass
class DeviceInfo:
    browsername: str
    browserversion: str
    osname: str
    type: str

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

email = ""

# Function to verify user email
def post_user_verify(email):
    url = "https://accounts.pronto.io/api/v1/user.verify"
    payload = {"email": email}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        raise BackendError(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise BackendError(f"An error occurred: {err}")

# Function to log in using email and verification code
def token_login(email, verification_code):
    url = "https://accounts.pronto.io/api/v3/user.login"
    device_info = DeviceInfo(
        browsername="Firefox",
        browserversion="130.0.0",
        osname="Windows",
        type="WEB"
    )
    request_payload = {
        "email": email,
        "code": verification_code,
        "device": asdict(device_info)
    }
    headers = {
        "Content-Type": "application/json"
    }
    logger.info(f"Payload being sent: {request_payload}")
    try:
        response = requests.post(url, json=request_payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

# Function to save response data to a file
def save_response_to_file(response_data, file_path):
    try:
        with open(file_path, "w") as file:
            json.dump(response_data, file, indent=4)
        logger.info(f"Response data saved to {file_path}")
    except IOError as io_err:
        logger.error(f"File write error: {io_err}")

# Function to handle the verification code input and token login process
def verification_code_to_accessToken(email, verification_code):
    try:
        start_time = time.time()
        result = token_login(email, verification_code)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Time to get response: {total_time} seconds.")
        save_response_to_file(result, r"C:\Users\paul\Desktop\Better Pronto UI\JSON\accessTokenResponse.json")
        if result.get("ok"):
            logger.info(f"User authenticated: {result}")
            return True
        else:
            logger.error(f"Authentication failed: {result.get('error', 'Unknown error')}")
            return False
    except BackendError as e:
        logger.error(e)
        return False

# UI SECTION
# UI For Better Pronto
# Login/Verification Page

def submit_email(event=None):
    global email
    email = entry_email.get()
    # Check if the email contains @ohs.stanford.edu
    if "@ohs.stanford.edu" in email:
        print(f"Email: {email}")
        try:
            print("Requesting verification code for", email)
            request_start_time = time.time()
            result = post_user_verify(email)
            request_end_time = time.time()
            total_time = request_end_time - request_start_time
            print(f"Request took {total_time:.2f} seconds.")
            print("Verification email sent:", result)
            print(f"Please check {email} for the verification code.")
            show_verification_page()
        except BackendError as e:
            print(e)
            error_label = tk.Label(frame, text="Failed to send verification code.", fg="red", font=custom_font)
            error_label.grid(row=2, columnspan=2, pady=10)
    else:
        # Show error message and clear the entry field
        error_label = tk.Label(frame, text="Invalid email. Please use your @ohs.stanford.edu email", fg="red", font=custom_font)
        error_label.grid(row=2, columnspan=2, pady=10)
        entry_email.delete(0, tk.END)

def show_email_entry_page():
    global entry_email, frame, custom_font, root
    # Create the main window
    root = tk.Tk()
    root.title("Better Pronto 1.0")
    root.geometry("500x500")

    # Define a custom font
    custom_font = font.Font(family="Helvetica", size=12)

    # Create a frame for the email form
    frame = tk.Frame(root, padx=20, pady=20, bg="#f0f0f0")
    frame.pack(expand=True)

    # Email label and entry
    label_email = tk.Label(frame, text="Email:", font=custom_font, bg="#f0f0f0")
    label_email.grid(row=0, column=0, pady=10, padx=5, sticky="e")
    entry_email = tk.Entry(frame, width=40, font=custom_font)
    entry_email.grid(row=0, column=1, pady=10, padx=5)
    entry_email.bind("<Return>", submit_email)  # Bind Enter key to submit_email

    # Submit button
    button_submit = tk.Button(frame, text="Request Verification Code", command=submit_email, bg="#007acc", fg="white", font=custom_font, padx=10, pady=5)
    button_submit.grid(row=1, columnspan=2, pady=20)

    # Run the application
    root.mainloop()

def show_verification_page():
    global entry_code
    # Clear the frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Verification code label and entry
    label_code = tk.Label(frame, text=f"Enter 6-digit Verification Code Sent to {email}:", font=custom_font, bg="#f0f0f0")
    label_code.grid(row=0, column=0, columnspan=2, pady=10)
    entry_code = tk.Entry(frame, width=20, font=custom_font)
    entry_code.grid(row=1, column=0, columnspan=2, pady=10)

    # Submit button for verification code
    button_verify = tk.Button(frame, text="Verify Code", command=verify_code, bg="#007acc", fg="white", font=custom_font, padx=10, pady=5)
    button_verify.grid(row=2, column=0, columnspan=2, pady=20)

def verify_code():
    code = entry_code.get()
    # Process the verification code
    print(f"Verification Code: {code}")
    success = verification_code_to_accessToken(email, code)
    if success:
        success_label = tk.Label(frame, text="Verification successful!", fg="green", font=custom_font)
        success_label.grid(row=3, columnspan=2, pady=10)
        # Proceed to the next step or close the window
        root.after(2000, root.destroy)  # Close after 2 seconds
    else:
        error_label = tk.Label(frame, text="Verification failed. Please try again.", fg="red", font=custom_font)
        error_label.grid(row=3, columnspan=2, pady=10)

# Call the function to show the email entry page
if __name__ == "__main__":
    show_email_entry_page()
