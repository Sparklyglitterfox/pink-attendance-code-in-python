import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import calendar
from PIL import Image, ImageTk

class AttendanceSheet:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Sheet - Personal Project! :)))")
        self.root.configure(bg="#F0F0F0")  # Set background color

        # Load background image
        self.background_image = Image.open("background.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        
        # Set background image
        self.background_label = tk.Label(root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.last_marked_day = -1
        self.days = {}
        
        # Frame for the button to position it
        self.button_frame = tk.Frame(self.root, bg="#F0F0F0")
        self.button_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nw")

        # Load button image
        self.button_image = ImageTk.PhotoImage(file="button_image.png")
        self.attendance_button = tk.Button(self.button_frame, image=self.button_image, command=self.mark_attendance, borderwidth=0, bg='#F0F0F0', activebackground='#F0F0F0', bd=0, cursor="hand2")
        self.attendance_button.pack()

        self.initialize_days()

    def mark_attendance(self):
        now = datetime.now()
        today = now.day

        if today != self.last_marked_day:
            self.last_marked_day = today
            attendance_record = f"{now.strftime('%Y-%m-%d')}: present"
            self.save_attendance(attendance_record)
            self.update_day_canvas(today)
        else:
            messagebox.showinfo("Info", "Attendance already marked for today!")

    def save_attendance(self, attendance_record):
        try:
            with open("attendance.txt", "a") as file:
                file.write(attendance_record + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save attendance: {str(e)}")

    def initialize_days(self):
        now = datetime.now()
        year = now.year
        month = now.month
        days_in_month = calendar.monthrange(year, month)[1]

        calendar_frame = tk.Frame(self.root, bg="#F0F0F0")
        calendar_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nw")

        for i in range(days_in_month):
            day_frame = tk.Frame(calendar_frame, bg="#F0F0F0")
            day_frame.grid(row=i // 7, column=i % 7, padx=5, pady=5)

            day_label = tk.Label(day_frame, text=str(i + 1), font=("Arial", 12, "bold"), bg="#F0F0F0")
            day_label.pack()

            day_frame.bind("<Button-1>", lambda event, day=i+1: self.mark_attendance())
            self.days[i + 1] = {"frame": day_frame, "label": day_label}

    def update_day_canvas(self, today):
        if today in self.days:
            self.days[today]["label"].configure(text="Present", fg="green")
            self.days[today]["frame"].configure(bg="#C0FAC0")  # Change color to indicate attendance marked

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")  # Set the window size to fit the background image
    attendance_sheet = AttendanceSheet(root)
    root.mainloop()
