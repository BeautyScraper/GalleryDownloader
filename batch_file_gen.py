import os
import subprocess

def execute_python_file(file_name):
    try:
        subprocess.run(["python", file_name], check=True)
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing '{file_name}':")
        print(e)

def main():
    current_directory = os.getcwd()
    file_list = [file for file in os.listdir(current_directory) if file.endswith(".py")]
    
    if not file_list:
        print("No Python files found in the current directory.")
        return

    print("Python files in the current directory:")
    for idx, file_name in enumerate(file_list, start=1):
        print(f"{idx}. {file_name}")

    user_choice = input("Enter the number corresponding to the file you want to execute (or 'q' to quit): ")
    if user_choice.lower() == 'q':
        return

    try:
        file_index = int(user_choice) - 1
        selected_file = file_list[file_index]
        execute_python_file(selected_file)
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid file number.")
        main()

if __name__ == '__main__':
    main()
