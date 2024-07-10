import os
import csv
from time import sleep
from datetime import datetime
from collections import deque
import run_ocr
import tracker
import sys

# define the keywords and the directory to search
keyword1 = "Mekel,SUCCESS"
keyword2 = "Mekel,save"
directory_to_search = 'path_to_directory'  # Change this to the directory you want to search
csv_file_path = 'processed_files.csv'

# Function to get the list of already processed files
def get_processed_files(csv_file):
    if not os.path.exists(csv_file):
        return []
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        return [row[0] for row in reader]


# Function to save new files to the CSV
def save_to_csv(new_files, csv_file):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file, quotechar=',')
        writer.writerows(new_files)


# Function to search for the keyword in text files
def search_keyword_in_files(directory, keyword1, keyword2, processed_files):
    """
    Searches for a specific keyword combination in text files within a directory.

    Args:
        directory (str): The directory to search for text files.
        keyword1 (str): The first keyword to search for.
        keyword2 (str): The second keyword to search for.
        processed_files (list): A list of file paths that have already been processed.

    Returns:
        list: A list of file paths and timestamps where the keyword combination was found.
    """
    new_files = []
    keyword1_words = keyword1.split(',')
    keyword2_words = keyword2.split()

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
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
    return new_files


# Helper function to save completion time and src_path to a CSV file
def save_completion_time(src_path, time_taken):
    completion_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
    with open('completion_times.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([src_path, completion_time, time_taken])


# run automation script if there are jobs in queue
def get_jobs_in_queue(que):
    if que:  # check if there are jobs in queue
        curr = que.pop()  # current location of the folder to be processed.
        run_ocr.open_OCR()  # open OCR
        run_ocr.run(curr)  # run the 0th script
        print(f"Current directory being processed: {curr}")

        start = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        tracker.look_for_completion(curr)  # runs for the whole duration of the OCR process
        end = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        time_taken = datetime.strptime(end, '%m/%d/%Y %I:%M:%S %p') - datetime.strptime(start, '%m/%d/%Y %I:%M:%S %p')

        print(f"Time taken to complete: {time_taken}")
        print("-------------------------")

        save_completion_time(curr, time_taken)  # save the completion time to a CSV file
    if que:
        get_jobs_in_queue(que)  # recursively call the function to check for more jobs in queue


if __name__ == '__main__':

    # Get already processed files
    processed_files = get_processed_files(csv_file_path)

    # Search for keyword in files
    new_files = search_keyword_in_files(directory_to_search, keyword1, keyword2, processed_files)

    # Save new files to CSV
    if new_files:
        save_to_csv(new_files, csv_file_path)

    # Output new files found
    print("New jobs found:")

    # create a queue to store the jobs
    global que
    que = deque()
    for new_file in new_files:
        addy = str(new_file[0]).rsplit('\\', 1)[0]
        print(addy)
        que.append(addy)

    if not que:
        print('None')
        sleep(1)
        print('Exiting...')
        sleep(3)  # sleep for 60 seconds before checking for new jobs
    if que:
        s = input("Start? Type y/n: ")
        if s == 'n':  # get rid of the processed files from the csv and end the program
            sys.exit()
        if s == 'y':
            get_jobs_in_queue(que)

