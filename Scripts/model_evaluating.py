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

def evaluate(username, model, gh):
    while(1):
        repo = input('Please enter the GitHub repository: ') # Example: GitHub_Auto-Labeler
        if(repo.strip().lower() == 'exit'):
            break
        issue = input('Please enter the GitHub issue #: ')
        if(issue.strip().lower() == 'exit'):
            break
        
 
        try:
            issue = gh.issue(username, repo, issue)
            print(f'Found issue: {issue.title}')
            text = issue.title + '. ' + issue.body
            
            labels = issue.labels()
            print('Current labels: ')
            for label in labels:
                print(label)

            temp_output = model.predict(pd.DataFrame([text]))
            output = tf.nn.softmax(temp_output)
            prediction = np.argmax(output, axis=1)
            print('Prediction label is : ' + ['bug', 'feature', 'question'][int(prediction)])

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
