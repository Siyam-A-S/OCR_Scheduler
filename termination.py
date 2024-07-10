# import keyboard
# import os
#
# # implement a script that terminates the program when a key is pressed
#
# def terminate_program():
#     print("Terminating program...")
#     os._exit(0)
#
#     # Close all instances of quantumOCR upon termination
#
#     def close_all_instances():
#         os.system("taskkill /f /im quantumOCR.exe")
#     close_all_instances()
#
# def exit_hotkey():
#     keyboard.add_hotkey('ctrl+q', terminate_program)
#
