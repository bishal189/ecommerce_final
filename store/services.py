import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import models
from sentence_transformers import SentenceTransformer
import pickle

# load data and prepare data


def load_data(data):
    return pd.read_csv(data)


def prepare_data(df):
    docx = df['product_name'].tolist()
    payload = df[['id','product_name', 'images','stock','price','is_available','slug', 'description']].to_dict('records')
    return docx, payload


def save_vectors(vectors):
    with open('vectorized_courses.pickle', 'wb') as f:
        pickle.dump(vectors, f)


def load_vectors(vector_file):
    with open(vector_file, 'rb') as f:
        myobject = pickle.load(f)
    return myobject


# create a vector db client
#
client = QdrantClient(path='vector_database.db')
client.recreate_collection(collection_name='product_collection',
                           vectors_config=models.VectorParams(
                               size=384, distance=models.Distance.COSINE
                           ))


# vectorized our data create word embedaded


model = SentenceTransformer('all-MiniLM-L6-v2')
df = load_data('data1.csv')
docx, payload = prepare_data(df)
print(docx)
vectors = model.encode(docx, show_progress_bar=True)
save_vectors(vectors)

# payload_list = payload.to_dict(orient='records')
# store in vectore db collection

client.upload_collection(
    collection_name='product_collection',
    vectors=vectors,
    payload=payload,
    ids=None,
    batch_size=256

)

vectorized_text = model.encode('python').tolist()
results = client.search(collection_name='product_collection',
                        query_vector=vectorized_text, limit=5)


# print(results)
