# OCR Scheduler
This is a utility program for Quantum Software Suite used for microfilm scanning, OCR and digitization. This is a python script to recognize jobs ready for OCR coming from Quantum Process (after annotation) and pass them into Optical Character Recognition (uses tesseract) in batch automatically overnight on QuantumOCR/pytesseract. Overnight batch jobs save time and effort of the Quality Control and Post Processing as OCR takes up a lot of time.

Anyone can use it for scheduling tasks and automating mouse clicks and keyboard controls after identifying the trigger for their specific software. Documentation will be made further to support code manipulation.



#Quantum Software Suite
Link: https://thecrowleycompany.com/scanner-products/software/mekel-technology-quantum/

#Documentaion

This script provides an OCR automation tool with a graphical user interface (GUI) built using Tkinter.
The script allows users to search for specific keywords in files within a selected directory and perform OCR (Optical Character Recognition) on the found files.
The script also provides functionality to schedule the OCR process at a specific time.
Functions:
- get_processed_files(csv_file): Retrieves the list of already processed files from a CSV file.
- save_to_csv(new_files, csv_file): Saves new files to the CSV file.
- search_keyword_in_files(directory, keyword1, keyword2, processed_files): Searches for files containing specific keywords in the given directory.
- save_completion_time(src_path, time_taken): Saves the completion time of the OCR process to a CSV file.
- get_jobs_in_queue(que, log_text_widget): Runs the OCR process for jobs in the queue.
- Application: Represents the main GUI application class.
Classes:
- Application: Represents the main GUI application class.
Usage:
1. Run the script.
2. Select a directory to search for files.
3. Click the "Search for Jobs" button to search for files containing specific keywords.
4. If new files are found, they will be displayed in the "Jobs Found" listbox.
5. Click the "Start OCR" button to start the OCR process for the selected jobs.
6. The status of the OCR process will be displayed in the "Status" text area.
7. Completed jobs will be displayed in the "Completed Jobs" listbox.
8. To remove a completed job from the list, select the job and click the "Remove Selected File" button.
9. To schedule the OCR process at 4:00 PM, click the "Schedule OCR at 4:00 PM" button.
Note: This script requires the following dependencies: os, csv, datetime, collections, run_ocr, tracker, tkinter, threading, filedialog, messagebox, ttk, scrolledtext.
