import os
import subprocess

def execute_python_file(file_name):
    try:
        if 'c__' in file_name:
            condaenv_name = file_name.split('c__')[-1].split('.')[0]
            os.system(' '.join(["conda", "activate", condaenv_name,"&&", "python", file_name]))
        else:
            subprocess.run(["python", file_name], check=True)
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing '{file_name}':")
        print(e)

def main():
    directory = os.getcwd()
    python_files = [file for file in os.listdir(directory) if file.endswith(".py")]
    
    if not python_files:
        return

    display_file_list(python_files)

    user_choice = get_user_input()


    for choice in user_choice:
        execute_selected_file(choice, python_files)



def display_file_list(files):
    print("Python files in the current directory:")
    for i, file_name in enumerate(files, start=1):
        print(f"{i}. {file_name}")


def get_user_input():
    while True:
        choice = input("Enter the number corresponding to the file you want to execute (or 'q' to quit) or \nyou may also combine multiple inputs seperated by space:")
        choice = choice.split()
        try:
            return choice
        except ValueError:
            print("Invalid input. Please enter a valid file number.")



def execute_selected_file(choice, files):
    if choice == 'r':
        last_five_files = files[-5:]
        display_file_list(last_five_files)
        return get_user_input()

    selected_file = files[int(choice) - 1]
    execute_python_file(selected_file)


if __name__ == '__main__':
    main()


if __name__ == '__main__':
    main()
