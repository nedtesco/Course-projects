# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
#'''This code reads usernames and password from the user.txt file to 
#allow a user to login.'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


#====Defining menu functions====
def reg_user():
    '''Add a new user to the user.txt file'''
    while True:
        # - Request input of a new username
        new_username = input("New Username: ")

        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the username doesn't already exist
        if new_username in username_password.keys():
            print("Error: Username already exist, please try another.")
        else:
            # - Check if the new password and confirmed password are the same.
            if new_password == confirm_password:
                # - If they are the same, add them to the user.txt file,
                print("New user added")
                username_password[new_username] = new_password

                with open("user.txt", "w") as out_file:
                    user_data = []
                    for k in username_password:
                        user_data.append(f"{k};{username_password[k]}")
                    out_file.write("\n".join(user_data))
                break
            # - Otherwise you present a relevant message.
            else:
                print("Passwords do not match, please try again.")


def add_task():
    '''Allow a user to add a new task to task.txt file
    Prompt a user for the following: 
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task and 
    - the due date of the task.'''
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
        else:
            task_title = input("Title of Task: ")
            task_description = input("Description of Task: ")
            while True:
                try:
                    task_due_date = input("Due date of task (YYYY-MM-DD): ")
                    due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                    break

                except ValueError:
                    print("Invalid datetime format. Please use the format specified")


            # Then get the current date.
            curr_date = date.today()
            # - Add the data to the file task.txt and
            # - include 'No' to indicate if the task is complete.
            new_task = {
                "username": task_username,
                "title": task_title,
                "description": task_description,
                "due_date": due_date_time,
                "assigned_date": curr_date,
                "completed": False
            }

            task_list.append(new_task)
            with open("tasks.txt", "w") as task_file:
                task_list_to_write = []
                for t in task_list:
                    str_attrs = [
                        t['username'],
                        t['title'],
                        t['description'],
                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                        "Yes" if t['completed'] else "No"
                    ]
                    task_list_to_write.append(";".join(str_attrs))
                task_file.write("\n".join(task_list_to_write))
            print("Task successfully added.")
            break


def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling) 
    '''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


def view_mine():
    '''Reads the task from task.txt file and allows the user
    to mark tasks as complete, or make changes to the task's
    user or due date'''

    def vm_edit():
        '''Allows the user to edit the username or the due date
        of the task they have selected'''
        while True:
            ed_choice = input('''Select one of the following options below:
user - Change the username to whom the task is assigned
date - Change the task's due date
>''').lower()
            if ed_choice == "user":
                new_user = input("""Please input the username of the person
to whom the task is now assigned.
>""")
                if new_user not in username_password.keys():
                    print("User does not exist, please enter a valid username.")
                else:
                    # Updating the task on the file task.txt
                    task_list[vm_choice-1]['username'] = new_user
                    print("Task's user has been updated.")
                    break

            elif ed_choice == "date":
                # Updating the due date and storing to be written to the text file
                while True:
                    try:
                        task_due_date = input("Due date of task (YYYY-MM-DD): ")
                        due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                        print("Task's due date has been updated.")
                        break

                    except ValueError:
                        print("Invalid datetime format. Please use the format specified")

                task_list[vm_choice-1]['due_date'] = due_date_time
                break

            else:
                print("Invalid input, please try again.")

        # Writing the new updates to the text file
        with open("tasks.txt", "w") as task_file:
            updated_tasks = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                updated_tasks.append(";".join(str_attrs))
            task_file.write("\n".join(updated_tasks))
        print("Task successfully updated.")


    task_num = {}

    # Assigning a numerical value to each task which the user can then input to access
    for num, t in enumerate(task_list, start=1):
        if t['username'] == curr_user:
            disp_str = f"Task {num}: \t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            task_num[num] = t
            print(disp_str)

    while True:
        vm_choice = int(input("""Please select a task by inputting its task number,
or enter '-1' to return to main menu\n>"""))
        if vm_choice == -1:
            break
        else:
            if vm_choice not in task_num.keys():
                print("Input does not match task numbers, please try again.")
            else:
                vm_menu = input('''Select one of the following options below:
tc - Mark the task as complete
ed - Edit the task's user or due date
>''').lower()
                if vm_menu == "tc":
                    # Updating the completion status and writing it to the text file
                    with open("tasks.txt", "w") as task_file:
                        task_list[vm_choice-1]['completed'] = True
                        updated_tasks = []
                        for t in task_list:
                            str_attrs = [
                                t['username'],
                                t['title'],
                                t['description'],
                                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                "Yes" if t['completed'] else "No"
                            ]
                            updated_tasks.append(";".join(str_attrs))
                        task_file.write("\n".join(updated_tasks))
                    print("Task marked as completed.")
                elif vm_menu == "ed":
                    if task_list[vm_choice-1]['completed'] is True:
                        print("This task has been completed and cannot be edited.")
                    else:
                        vm_edit()


def task_report():
    """Generates a text file report on completion status of tasks, including the
    number of completed, uncompleted, and overdue tasks"""
    comp_tasks = 0
    uncomp_tasks = 0
    overdue_tasks = 0
    curr_date = date.today().strftime(DATETIME_STRING_FORMAT)

    # Running through the tasks and storing their completion data
    for count, t in enumerate(task_list):
        if task_list[count]['completed'] is True:
            comp_tasks += 1
        elif task_list[count]['completed'] is False:
            uncomp_tasks += 1
            if task_list[count]['due_date'] > datetime.strptime(curr_date, DATETIME_STRING_FORMAT):
                overdue_tasks += 1

    # Storing the task data to be put in the report
    t_ovv = f"Total tasks: \t\t {len(task_list)}\n\n"
    t_ovv += f"Completed tasks: \t {comp_tasks}\n"
    t_ovv += f"Uncompleted tasks: \t {uncomp_tasks}\n"
    t_ovv += f"Overdue tasks:  \t {overdue_tasks}\n\n"
    t_ovv += "Percentage completed:\t"
    t_ovv += f"{comp_tasks/(len(task_list))*100}%\n" if len(task_list) > 0 else " 0%\n"
    t_ovv += "Percentage uncompleted:\t"
    t_ovv += f"{uncomp_tasks/(len(task_list))*100}%\n" if len(task_list) > 0 else " 0%\n"
    t_ovv += "Percentage overdue:\t\t"
    t_ovv += f"{overdue_tasks/(len(task_list))*100}%\n" if len(task_list) > 0 else " 0%\n"

    with open("task_overview.txt", "w") as task_ovv:
        task_ovv.write(t_ovv)


def user_report():
    """Generates a text file report on user tasks and their completion status"""
    u_ovv = f"Total users: \t\t {len(username_password)}\n"
    u_ovv += f"Total tasks: \t\t {len(task_list)}\n\n"
    curr_date = date.today().strftime(DATETIME_STRING_FORMAT)

    # Running through the users to add to the list and count their tasks
    for u in username_password.keys():
        u_ovv += f"User:\t\t\t\t\t{u}\n"
        user_tasks = 0
        user_comp = 0
        user_uncomp = 0
        user_overdue = 0

        for count, t in enumerate(task_list):
            if task_list[count]['username'] == u:
                user_tasks += 1
                if task_list[count]['completed'] is True:
                    user_comp += 1
                elif task_list[count]['completed'] is False:
                    user_uncomp += 1
                    if task_list[count]['due_date'] > datetime.strptime(curr_date, DATETIME_STRING_FORMAT):
                        user_overdue += 1

        # Storing the task data of the users to be put in the report
        u_ovv += f"User assigned tasks:\t{user_tasks}\n"
        u_ovv += "Percentage of total:\t"
        u_ovv += f"{user_tasks/(len(task_list))*100}%\n" if len(task_list) > 0 else " 0%\n"
        u_ovv += "Percentage completed:\t"
        u_ovv += f"{(user_comp/user_tasks)*100}%\n" if user_tasks > 0 else " 0%\n"
        u_ovv += "Percentage uncompleted:\t"
        u_ovv += f"{(user_uncomp/user_tasks)*100}%\n" if user_tasks > 0 else " 0%\n"
        u_ovv += "Percentage overdue:\t\t"
        u_ovv += f"{(user_overdue/user_tasks)*100}%\n\n" if user_tasks > 0 else " 0%\n\n"

    with open("user_overview.txt", "w") as user_ovv:
        user_ovv.write(u_ovv)


def display_stats():
    '''If the user is an admin they can display statistics about number of users
        and tasks'''
    with open("user.txt", "r") as user_doc:
        num_users = len(user_doc.readlines())
    with open("tasks.txt", "r") as task_doc:
        num_tasks = len(task_doc.readlines())

    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")



while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'gr' and curr_user == 'admin':
        task_report()
        user_report()
        print("Reports have been generated.")

    elif menu == 'ds' and curr_user == 'admin':
        display_stats()
    
    elif menu == 'gr' or 'ds' and curr_user != 'admin':
        print("Choice invalid - admin required to access this option.")

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
