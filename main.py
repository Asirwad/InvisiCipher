import customtkinter as ctk
from PIL import Image, ImageTk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.geometry("1000x700")
root.title("InvisiCipher")

# Create a frame for the login page
loginFrame = ctk.CTkFrame(root, width=1000, height=700, bg_color="black")
loginFrame.place(relx=0.5, rely=0.5, anchor="center")

# Add labels for the app name and user login
appNameLabel = ctk.CTkLabel(loginFrame, text="InvisiCipher", font=("Helvetica", 40, "bold"), fg_color="#333333", bg_color="white")
appNameLabel.place(relx=0.5, rely=0.1, anchor="center")

userLoginLabel = ctk.CTkLabel(loginFrame, text="User Login", font=("Helvetica", 32, "bold"), fg_color="#333333", bg_color="white")
userLoginLabel.place(relx=0.5, rely=0.25, anchor="center")

# Add an icon next to the app name label
image = Image.open("icons/logo.png")
photo = ImageTk.PhotoImage(image)
imageLabel = ctk.CTkLabel(root, image=photo, text="App Name")
imageLabel.place(relx=0.3, rely=0.1, anchor="center")

# Add CTkEntries for username and password
username_entry = ctk.CTkEntry(loginFrame, font=("Helvetica", 24), fg_color="#333333", bg_color="#f2f2f2", placeholder_text="Username")
username_entry.place(relx=0.5, rely=0.45, anchor="center")

password_entry = ctk.CTkEntry(loginFrame, font=("Helvetica", 24), fg_color="#333333", bg_color="#f2f2f2", placeholder_text="Password", show="*")
password_entry.place(relx=0.5, rely=0.55, anchor="center")

# Add a login button
login_button = ctk.CTkButton(loginFrame, text="Login", font=("Helvetica", 24), fg_color="#ffffff", bg_color="#333333")
login_button.place(relx=0.5, rely=0.7, anchor="center")

root.mainloop()
