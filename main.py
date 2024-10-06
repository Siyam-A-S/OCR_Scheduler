import os
import csv
from datetime import datetime, timedelta
from collections import deque
import run_ocr
import tracker
import tkinter as tk
import threading
from tkinter import filedialog, messagebox, ttk, scrolledtext


# define the keywords and the directory to search
keyword1 = "Mekel,SUCCESS"
keyword2 = "Mekel,save"
csv_file_path = 'Completed Jobs.csv'


# Function to get the list of already processed files
def get_processed_files(csv_file):
    if not os.path.exists(csv_file):
        return []
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        return [row[0] for row in reader if row and row[0]]  # Check for rows that are not empty and return the list of files


# Function to save new files to the CSV
def save_to_csv(new_files, csv_file):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        #print(new_files)
        writer.writerows(new_files)

def search_keyword_in_files(directory, keyword1, keyword2, processed_files):
    new_files = []
    keyword1_words = keyword1.split(',')
    keyword2_words = keyword2.split()

    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith('process.log.txt'):
                    with open(file_path, 'r') as f:
                        contents = f.read()
                        if "SUCCESS" in contents:
                            users_log_path = os.path.join(root, "users.log.txt")
                            if users_log_path not in processed_files:
                                timestamp = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
                                new_files.append([users_log_path, timestamp])
                                break

                elif file.endswith('users.log.txt'):
                    if file_path not in processed_files:
                        with open(file_path, 'r') as f:
                            lines = f.readlines()
                            for i in range(len(lines) - 1):
                                first_line_words = lines[i].split(',')[:2]
                                second_line_words = lines[i + 1].strip().split()[:1]
                                if (first_line_words == keyword1_words and
                                        second_line_words == keyword2_words):
                                    timestamp = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
                                    new_files.append([file_path, timestamp])
                                    break
    except Exception as e:
        print(f"Directory not searchable")
    return new_files


def save_completion_time(src_path, time_taken):
    completion_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
    with open('Completion times.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([src_path, completion_time, time_taken])


# Run automation script if there are jobs in queue
def get_jobs_in_queue(que, log_text_widget):
    if que:
        curr = que.pop()
        run_ocr.open_OCR()
        run_ocr.run(curr)
        log_text_widget.insert(tk.END, f"Current directory being processed: {curr}\n")
        log_text_widget.yview(tk.END)

        start = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        tracker.look_for_completion(curr)
        end = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        time_taken = datetime.strptime(end, '%m/%d/%Y %I:%M:%S %p') - datetime.strptime(start, '%m/%d/%Y %I:%M:%S %p')
        log_text_widget.insert(tk.END, f"Time taken to complete: {time_taken}\n")
        log_text_widget.insert(tk.END, "-------------------------\n")
        log_text_widget.yview(tk.END)

        save_completion_time(curr, time_taken)
        if que:
            get_jobs_in_queue(que, log_text_widget)


# Tkinter GUI
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OCR Automation")
        self.geometry("800x1200")
        self.configure(bg="#fef9f9")  # Set background color
        self.directory_to_search = None
        self.new_files = []
        self.processed_files = get_processed_files(csv_file_path)
        self.que = deque()

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style(self)
        style.theme_use('clam')  # Use 'clam' theme for a modern look

        # Configure styles
        style.configure('TButton', font=('Helvetica', 10), padding=6)
        style.configure('TLabel', font=('Helvetica', 10), background='#f0f0f0')
        style.configure('TEntry', font=('Helvetica', 10))
        style.configure('TListbox', font=('Helvetica', 10))
        style.configure('TScrolledText', font=('Helvetica', 10))

        self.directory_label = ttk.Label(self, text="Directory to Search:")
        self.directory_label.pack(pady=10)

        self.directory_entry = ttk.Entry(self, width=80)
        self.directory_entry.pack(pady=5)

        self.browse_button = ttk.Button(self, text="Browse", command=self.browse_directory)
        self.browse_button.pack(pady=5)

        self.search_button = ttk.Button(self, text="Search for Jobs", command=self.search_for_jobs)
        self.search_button.pack(pady=5)

        self.jobs_list_label = ttk.Label(self, text="Jobs Found")
        self.jobs_list_label.pack(pady=10)

        self.jobs_listbox = tk.Listbox(self, width=100, height=10, font=('Helvetica', 10))
        self.jobs_listbox.pack(pady=5)

        self.start_button = ttk.Button(self, text="Start OCR", command=self.start_ocr, state=tk.DISABLED)
        self.start_button.pack(pady=10)

        self.schedule_button = ttk.Button(self, text="Schedule OCR at 4:00 PM", command=self.schedule_ocr)
        self.schedule_button.pack(pady=10)

        self.log_label = ttk.Label(self, text="Status")
        self.log_label.pack(pady=10)

        self.log_text = scrolledtext.ScrolledText(self, width=100, height=10, state=tk.DISABLED, font=('Helvetica', 10))
        self.log_text.pack(pady=5)

        self.processed_files_label = ttk.Label(self, text="Completed Jobs")
        self.processed_files_label.pack(pady=10)

        self.processed_files_listbox = tk.Listbox(self, width=100, height=10, font=('Helvetica', 10))
        self.processed_files_listbox.pack(pady=5)

        # Add the remove button
        self.remove_button = ttk.Button(self, text="Remove Selected File", command=self.remove_selected_file)
        self.remove_button.pack(pady=10)

    def browse_directory(self):
        self.directory_to_search = filedialog.askdirectory()
        self.directory_entry.delete(0, tk.END)
        self.directory_entry.insert(0, self.directory_to_search)

    def search_for_jobs(self):
        if not self.directory_to_search:
            messagebox.showerror("Error", "Please select a directory to search.")
            return

        self.new_files = search_keyword_in_files(self.directory_to_search, keyword1, keyword2, self.processed_files)
        if self.new_files:  # If new files are found
            save_to_csv(self.new_files, csv_file_path)
            self.update_jobs_listbox()
            self.start_button.config(state=tk.NORMAL)
            self.search_button.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Info", "No new jobs found.")

    def update_jobs_listbox(self):
        self.jobs_listbox.delete(0, tk.END)
        self.que = deque()
        for new_file in self.new_files:
            addy = str(new_file[0]).rsplit('\\', 1)[0]
            self.jobs_listbox.insert(tk.END, addy)
            self.que.append(addy)

    def update_processed_files_listbox(self):
        self.processed_files_listbox.delete(0, tk.END)
        for file in self.processed_files:
            addy = file.rsplit('\\', 1)[0]
            self.processed_files_listbox.insert(tk.END, addy)

    def start_ocr(self):
        if self.que:
            confirmation = messagebox.askyesno("Start OCR", "Do you want to start the OCR process?")
            if confirmation:
                self.run_ocr_threaded()

    def run_ocr_threaded(self):
        threading.Thread(target=self.run_ocr).start()

    def run_ocr(self):
        self.log_text.config(state=tk.NORMAL)
        get_jobs_in_queue(self.que, self.log_text)
        self.processed_files.extend([file[0] for file in self.new_files])
        self.update_processed_files_listbox()
        self.log_text.insert(tk.END, "OCR process completed.\n")
        self.log_text.yview(tk.END)
        self.log_text.config(state=tk.DISABLED)  # Disable text widget
        self.start_button.config(state=tk.DISABLED)
        messagebox.showinfo("Info", "OCR process completed.")

    def schedule_ocr(self):
        schedule_time = datetime.now().replace(hour=16, minute=00, second=20, microsecond=0)
        now = datetime.now()

        if schedule_time < now:
            schedule_time += timedelta(days=1)

        delay = (schedule_time - now).total_seconds()

        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END,
                             f"OCR process scheduled to start at {schedule_time.strftime('%m/%d/%Y %I:%M:%S %p')}. Don't close the window.\n")
        self.log_text.yview(tk.END)
        self.log_text.config(state=tk.DISABLED)

        threading.Timer(delay, self.run_ocr_threaded).start()
        self.schedule_button.config(state=tk.DISABLED)

    def remove_selected_file(self):
        selected_idx = self.processed_files_listbox.curselection()
        if selected_idx:
            selected_file = self.processed_files_listbox.get(selected_idx[0])
            qocr_done_path = selected_file+"/frames/qocr-done.txt"
            confirmation = messagebox.askyesno("Remove File", f"Do you want to remove {selected_file} from the processed list?")
            if confirmation:
                self.processed_files.pop(selected_idx[0])
                #add the code to delete the qocr-done.txt file, trigger for qocr.exe that file has been OCR'd already
                if os.path.isfile(qocr_done_path):
                    try:
                        os.remove(qocr_done_path)
                    except PermissionError:
                        print(f"Permission denied: Unable to delete '{qocr_done_path}'.")
                self.update_processed_files_listbox()
                self.save_processed_files_to_csv()
                messagebox.showinfo("Info", f"{selected_file} has been removed from the processed list.")

    def save_processed_files_to_csv(self):
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            for processed_file in self.processed_files:
                writer.writerow([processed_file])


if __name__ == '__main__':
    app = Application()
    app.update_processed_files_listbox()
    app.mainloop()



