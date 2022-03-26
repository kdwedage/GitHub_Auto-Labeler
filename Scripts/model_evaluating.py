from github3 import login
from getpass import getpass
import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_text

def gitHubLogin():
    print('Please enter your Github credentials')
    for i in range(3):
        try:
            username = input('GitHub username: ')
            password = getpass()
            return username, login(username, password)
        except:
            print('Username and password combination is incorrect.')

def getModel():  
    while(1):
        try:
            model_path = input('Please enter the saved model\'s path: ')
            if(model_path.strip().lower() == 'exit'):
                break
            model = tf.keras.models.load_model(model_path) # Example: /var/Scripts/664/Models/0
            print('Successfully found model.')
            return model
        except Exception as e:
            print('There was an error with the path specified.\n Make sure the path is to the entire folder for the model.')
            print(e)

def processIssue(gh, username, repo, issue_num, model, verbose = False):
    issue = gh.issue(username, repo, issue_num)
    if(verbose):
        print(f'Found issue: {issue.title}\n')
    text = issue.title + '. ' + issue.body
    
    labels = issue.labels()
    different_labels = []
    if (verbose):
        print('Current labels: ')
    
    for label in labels:
        if(verbose):
            print(label.name)
        if (label.name != 'bug' and label.name != 'feature' and label.name != 'question'):
            different_labels.append(label.name)
    
    temp_output = model.predict(pd.DataFrame([text]))
    output = tf.nn.softmax(temp_output)
    prediction = np.argmax(output, axis=1)
    prediction_class = ['bug', 'feature', 'question'][int(prediction)]
    if(verbose):
        print('\nPrediction label is : ' + prediction_class)
    return issue, prediction_class, different_labels


def evaluate(username, model, gh):
    while(1):
        repo = input('Please enter the GitHub repository: ') # Example: GitHub_Auto-Labeler
        repo = 'GitHub_Auto-Labeler'
        if(repo.strip().lower() == 'exit'):
            break
        
        scope = int(input('Please enter a number indicating the choice in options: \n'
            '0: A specific issue \n'
            '1: A range of issues \n'
            '2: Exit \n'
            ))
        
        if (scope == 0):
            issue_num = input('Please enter the GitHub issue #: ')
            if(issue_num.strip().lower() == 'exit'):
                break
        elif (scope == 1):
            min_issue = input('Please enter the minimum GitHub issue #: ')
            if(min_issue.strip().lower() == 'exit'):
                break
            max_issue = input('Please enter the maximum GitHub issue #: ')
            if(max_issue.strip().lower() == 'exit'):
                break
        elif (scope == 2):
            break
        else:
            print('Incorrect option')
            continue 
 
        try:
            if(scope == 0):

                option = int(input('\nPlease enter a number indicating the choice in options: \n'
                    '0: Add predicted label to issue \n'
                    '1: Update labels of issue (remove prior label) \n'
                    '2: Exit\n'
                    ))
                issue, prediction_class, different_labels = processIssue(gh, username, repo, issue_num, model, verbose = True)

                if(option == 0):
                    issue.add_labels(prediction_class)
                elif(option == 1):
                    different_labels.append(prediction_class)
                    issue.edit(labels=different_labels)
                elif(option == 2):
                    break
            else:
                option = int(input('\nPlease enter a number indicating the choice in options: \n'
                    '0: Add predicted label to each issue \n'
                    '1: Update labels of issue (remove prior labels) \n'
                    '2: Exit\n'
                    )) 
                
                for i in range(int(min_issue), int(max_issue) + 1):
                    issue, prediction_class, different_labels = processIssue(gh, username, repo, i, model)

                    if(option == 0):
                        issue.add_labels(prediction_class)
                    elif(option == 1):
                        different_labels.append(prediction_class)
                        issue.edit(labels=different_labels)
                    elif(option == 2):
                        break
        except Exception as e:
            print(f'Error getting issue from {repo}')
            print(e)
def main():
    print('GitHub Issues Auto-Labeler by Kevin Wedage')
    username, gh = gitHubLogin()
    model = getModel()
    evaluate(username, model, gh)
        
if __name__ == '__main__':
    main()
