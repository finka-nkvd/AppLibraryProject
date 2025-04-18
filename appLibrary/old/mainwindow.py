import customtkinter as ctk

def main():
    root = ctk.CTk()
    root.title("Customtkinter Centered Window")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    root.geometry(f"1920x1030+-7+-3")

    root.mainloop()
main()