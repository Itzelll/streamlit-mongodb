from pymongo import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
import plotly.express as px

# replace here with your mongodb url 
#uri = "mongodb+srv://adsoft:adsoft-sito@cluster0.kzghgph.mongodb.net/?retryWrites=true&w=majority"
uri = "mongodb+srv://itzelll:NtWMhS9DNb1RzPp0@comidas.tv394y9.mongodb.net/?retryWrites=true&w=majority"

# Connect to meme MongoDB database

try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    db = client.memes
    print("MongoDB Connected successfully!")
except:
    print("Could not connect to MongoDB")

# streamlit run streamlit-mongo.py --server.enableCORS false --server.enableXsrfProtection false

st.title("Estadisticas")
st.subheader("Abre el sidebar para ver las opciones")
# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    items = db.memes_info.find()
    items = list(items)  # make hashable for st.cache_data
    return items

items = get_data()

sidebar = st.sidebar
sidebar.title("Itzel Mendez Martinez")
sidebar.write("Matricula: S20006761")
sidebar.write("zs20006761@estudiantes.uv.mx")
sidebar.markdown("___")

#
agree = sidebar.checkbox("Ver resultados en tabla ? ")
if agree:
    st.header("Resultados...")
    st.dataframe(items)
    st.markdown("___")
    
agree = sidebar.checkbox("Ver resultados raw ? ")
if agree:
    st.header("Resultados...")
    st.write(items)
    st.markdown("___")
    
#::::::::::: grafica de barras :::::::::::
#
"""
    agree = sidebar.checkbox("Clic para ver estadisticas de reacciones")
if agree:
    st.header("Grafica de barras")
    index=items.index
    reaction=items['name']
    fig_barra=px.bar(items,
                    x=index,
                    y=reaction,
                    orientation="v",
                    title="Total de reacciones",
                    labels=dict(reaction="Reacciones", index="Total"),
                    template="plotly_white")
    st.plotly_chart(fig_barra)
"""

#st.write('results...')
#st.write(items)

# Print results.i
#for item in items:
#    st.write(f"{item['_id']} has a :{item['name']}:")
