#!/usr/bin/env python3
import os
import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode('utf-8')}")
        return None

def get_current_git_user():
   
    current_user = run_command('git config --global user.name')
    current_email = run_command('git config --global user.email')
    return current_user, current_email

def update_git_credentials(new_user, new_email, account_type):
    
    run_command(f'git config --global user.name "{new_user}"')
    run_command(f'git config --global user.email "{new_email}"')

    
    message = f"Switched to {account_type} account: {new_user} with email: {new_email}"
    print(message)
    send_notification("Git Account Switch", message)

def send_notification(title, message):

    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])

def switch_git_user():

    personal_user = os.getenv("PERSONAL_USER")
    personal_email = os.getenv("PERSONAL_EMAIL")
    school_user = os.getenv("SCHOOL_USER")
    school_email = os.getenv("SCHOOL_EMAIL")

    


    current_user, current_email = get_current_git_user()

    if current_user == personal_user and current_email == personal_email:

        update_git_credentials(school_user, school_email, "school")
    elif current_user == school_user and current_email == school_email:

        update_git_credentials(personal_user, personal_email, "personal")
    else:

        print("Unrecognized Git user, switching to personal account by default.")
        update_git_credentials(personal_user, personal_email, "personal")

if __name__ == "__main__":
    switch_git_user()
