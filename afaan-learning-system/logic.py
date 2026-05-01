import pandas as pd
import random

# Load CSV file into a DataFrame
def load_vocab():
  return pd.read_csv("afaan-learning-system/data/vocab.csv")

def get_random_question(df: pd.DataFrame):
  return df.sample(1).iloc[0]

def check_answer(correct_answer, user_answer): 
  return correct_answer.strip().lower() == user_answer.strip().lower()