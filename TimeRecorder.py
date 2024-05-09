import os
import tkinter as tk
from tkinter import filedialog, messagebox
import datetime
import csv
from pathlib import Path

class TimeRecorder:
    def __init__(self, root):
        self.root = root
        self.start_time = None
        self.running = False
        self.total_duration = datetime.timedelta()  # to store total duration across pauses
        self.last_file_path = None

        # Setup GUI
        frame = tk.Frame(root)
        frame.pack(pady=10)

        self.start_button = tk.Button(frame, text="Start", command=self.start, width=10)
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = tk.Button(frame, text="Pause", command=self.pause, width=10)
        self.pause_button.grid(row=0, column=1, padx=5)

        self.stop_button = tk.Button(frame, text="Stop", command=self.stop, width=10)
        self.stop_button.grid(row=0, column=2, padx=5)

        self.reload_button = tk.Button(frame, text="Reload CSV", command=self.reload_csv, width=10)
        self.reload_button.grid(row=0, column=3, padx=5)

        # Text box for description
        text_frame = tk.Frame(root)
        text_frame.pack(pady=10)

        self.description_text = tk.Text(text_frame, height=2, width=50)
        self.description_text.grid(row=0, column=0, padx=5)

        # Example of adding another text box
        # self.additional_text = tk.Text(text_frame, height=5, width=25)
        # self.additional_text.grid(row=0, column=1, padx=5)
        
    def start(self):
        if not self.running:
            self.start_time = datetime.datetime.now()
            self.running = True
            print("Timer started or restarted")
    
    def pause(self):
        if self.running:
            self.end_time = datetime.datetime.now()
            self.running = False
            current_duration = self.end_time - self.start_time
            self.total_duration += current_duration
            print("Timer paused")
            print(f"Current Session Duration: {current_duration}")
            print(f"Total Recorded Time: {self.total_duration}")
    
    def stop(self):
        if self.running:
            self.pause()  # Ensure the last segment is added to total_duration if running

        description = self.description_text.get("1.0", tk.END).strip()
        if not description:
            messagebox.showwarning("Warning", "Please enter a description of what you did.")
            return
        
        if self.total_duration:
            print(f"Total time: {self.total_duration}")
            
            # Get user description
            description = self.description_text.get("1.0", tk.END).strip()
            file_path = filedialog.asksaveasfilename(filetypes=[("CSV Files", "*.csv")])
            if file_path:
                self.save_to_csv(file_path, self.total_duration, description)
                self.last_file_path = file_path
            
            # Reset
            self.start_time = None
            self.end_time = None
            self.total_duration = datetime.timedelta()
            self.description_text.delete('1.0', tk.END)
    
    def save_to_csv(self, file_path, time_spent, description):
        file_is_new = not Path(file_path).exists() or Path(file_path).stat().st_size == 0
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file_is_new:
                writer.writerow(["Time Spent", "Description"])  # Writing header
            writer.writerow([str(time_spent), description])
        print("Saved to CSV")
    
    def reload_csv(self):
        if self.last_file_path and Path(self.last_file_path).exists():
            # If there is a last file path and it exists, open it
            os.startfile(self.last_file_path)
        else:
            # If no last file path exists, create a new one with a header
            new_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], initialfile="NewTimeRecords.csv")
            if new_file_path:
                with open(new_file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Time Spent", "Description"])
                self.last_file_path = new_file_path
                print("New CSV file created with headers.")
                messagebox.showinfo("Info", "New CSV file created with headers.")
    
def main():
    root = tk.Tk()
    root.title("Time Recorder")
    app = TimeRecorder(root)
    root.mainloop()

if __name__ == "__main__":
    main()
