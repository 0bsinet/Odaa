import pandas as pd

# Load CSV file into a DataFrame
def load_vocab():
  return pd.read_csv("afaan-learning-system/data/vocab.csv")

# Return a random row in vocab.csv as a Series
def get_random_question(df: pd.DataFrame) -> pd.Series:
  return df.sample(1).iloc[0]

def check_answer(correct_answer: str, user_answer: str) -> bool: 
  return correct_answer.strip().lower() == user_answer.strip().lower()