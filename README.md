# GitHub_Auto-Labeler


A tool for automatically labeling GitHub issues using BERT. The main model in this project was trained using the dataset provided in reference 1.


# Requirements

List requirements here.

# Instructions

Docker stuff...

# Files

The Scripts directory contains all the python scripts for this project. 


## Scripts/model_training.py

This file is dedicated to determing the best parameters (hyperparameters) for the model used in this project.
In this project I explored various versions of BERT and various dropout values.

It is important to note that on line 9, 51 and 55 specific paths are used in order to refer to the original dataset, the location to save the models and the location to save the results. Please change these values to match your file structure. 

## Scripts/model_evaluating.py

This file is dedicated to evaluating a given model on a GitHub repository. Prior to running this file, a path to a saved model must be acquired, using the model_training.py file.   

## Scripts/performance_comparison.py

This file is intended to create GitHub issues and compare the performance of the saved model passed into it, with the alternative implementation found on GitHub marketplace, under larrylawl/Auto-Github-Issue-Labeller.

It is important to note that the alternative implementation was trained on a different training dataset and does not have entirely the same output classes (GitHub issue labels). 


# References:

- https://www.kaggle.com/arbazkhan971/github-bugs-prediction-challenge-machine-hack

- https://www.tensorflow.org/text/tutorials/classify_text_with_bert

- https://www.youtube.com/watch?v=D9yyt6BfgAM&ab_channel=codebasics
