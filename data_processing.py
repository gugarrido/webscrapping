import json
import pandas as pd

def read_data():
    dep_df = pd.read_json('deputados_dict.json')
    dep_df.index = pd.Index(['name','presence','absence_justified', 'absence_not_justified'], name='id')
    dep_df = dep_df.transpose(copy=True)
    dep_df.describe()


def main():
    read_data()
if __name__ == "__main__":
    main()