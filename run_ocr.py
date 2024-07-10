import os
import pyautogui
import pyperclip

def open_OCR():
    os.system('start "" "'+ "C:\QuantumOCR\qocr.exe"+'"')
    pyautogui.sleep(2)
    pyautogui.click(1014, 664)
    pyautogui.sleep(2)
    pyautogui.hotkey('win', 'up')
    #click on taskbar to bring the window to the front


def run(location): # run when the OCR software is not open

    # Text to copy
    text = location
    # Copy the text to the clipboard
    pyperclip.copy(text)

    pyautogui.moveTo(277, 96, duration=1.5)
    pyautogui.click(277, 96)# click on location bar

    pyautogui.sleep(1)
    pyautogui.hotkey('ctrl', 'a')# select all
    pyautogui.sleep(1)
    pyautogui.hotkey('ctrl', 'v')# paste the location

    pyautogui.moveTo(91, 478, duration=1)
    pyautogui.click(91, 478)  # click on the start button







