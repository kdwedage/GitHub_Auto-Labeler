from github3 import login
from getpass import getpass


def gitHubLogin():
    print('Please enter your Github credentials')
    for i in range(3):
        try:
            username = input('GitHub username: ')
            password = getpass()

            return login(username, password)
        except:
            print('Username and password combination is incorrect.')

def main():
    print('GitHub Issues Auto-Labeler by Kevin Wedage')
    gh = gitHubLogin()

    # Get the path to the saved model.
    # Get a repo that we want to check, and an issue (or multiple)
    # Then evaluate the model on the issue.
    # Several options: Evaluate a repo, update the labels on a repo, specify the specifc issues to change, or a range of them, or all.
    
        
if __name__ == '__main__':
    main()
