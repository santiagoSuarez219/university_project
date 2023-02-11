import tkinter as tk
import pandas as pd

def save_csv(data):
    df = pd.DataFrame(data)
    df.to_csv('data.csv', index=False)

