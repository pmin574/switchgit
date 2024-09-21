#!/usr/bin/env python3

import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode('utf-8')}")
        return None

def get_current_git_user():
    # Get current global Git username and email
    current_user = run_command('git config --global user.name')
    current_email = run_command('git config --global user.email')
    return current_user, current_email

def update_git_credentials(new_user, new_email, account_type):
    # Update global Git username and email
    run_command(f'git config --global user.name "{new_user}"')
    run_command(f'git config --global user.email "{new_email}"')

    # Notify the user via macOS notification
    message = f"Switched to {account_type} account: {new_user} with email: {new_email}"
    print(message)
    send_notification("Git Account Switch", message)

def send_notification(title, message):
    # Use AppleScript via osascript to trigger a macOS notification
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])

def switch_git_user():
    # Define your personal and school credentials
    personal_user = "pminne574"
    personal_email = "pminne574@gmail.com"

    school_user = "pjminne"
    school_email = "pjminne@iu.edu"

    # Check current Git user
    current_user, current_email = get_current_git_user()

    if current_user == personal_user and current_email == personal_email:
        # Switch to school account
        update_git_credentials(school_user, school_email, "school")
    elif current_user == school_user and current_email == school_email:
        # Switch to personal account
        update_git_credentials(personal_user, personal_email, "personal")
    else:
        # Handle case where no user is set or unknown credentials are found
        print("Unrecognized Git user, switching to personal account by default.")
        update_git_credentials(personal_user, personal_email, "personal")

if __name__ == "__main__":
    switch_git_user()
