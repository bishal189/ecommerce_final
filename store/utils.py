import pandas as pd
import pickle

# load data and prepare data


def load_data(data):
    return pd.read_csv(data)


def prepare_data(df):
    docx = df[['product_name','description']].values.tolist()
    payload = df[['id','product_name','description']].to_dict('records')
    return docx, payload


def save_vectors(vectors):
    with open('vectorized_courses.pickle', 'wb') as f:
        pickle.dump(vectors, f)


def load_vectors(vector_file):
    with open(vector_file, 'rb') as f:
        myobject = pickle.load(f)
    return myobject
