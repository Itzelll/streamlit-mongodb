from pymongo import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
import plotly.graph_objects as go
from pymongo import MongoClient
from collections import Counter

# replace here with your mongodb url 
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

st.title("Visualizacion de MongoDB")
# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    items = db.memes_reactions.find()
    items = list(items)  # make hashable for st.cache_data
    return items

items = get_data()

def mostrar():
    listasdb = db.memes_reactions.distinct("reactionId")
    listasdb = list(listasdb)
    return listasdb

print(mostrar())


items = get_data()

sidebar = st.sidebar
sidebar.title("Itzel Mendez Martinez")
sidebar.write("Matricula: S20006761")
sidebar.write("zs20006761@estudiantes.uv.mx")
sidebar.markdown("___")

#    
agree = sidebar.checkbox("Ver resultados raw (json) ? ")
if agree:
    st.header("Resultados...")
    st.write(items)
    st.markdown("___")

#
agree = sidebar.checkbox("Tabla de reactions")
if agree:
    st.header("Resultados...")
    st.dataframe(items)
    st.markdown("___")

############### reactions ################
if st.sidebar.checkbox('Grafica de barras reactions'):

    collection = db['memes_reactions']
    registros = collection.find()

    # Obtener los "reactionId" y contar la cantidad de cada uno
    reaction_ids = [registro['reactionId'] for registro in registros]
    contador_reaction_ids = Counter(reaction_ids)

    # Obtener los datos para la gráfica
    reaction_ids_list = list(contador_reaction_ids.keys())
    cantidad_list = list(contador_reaction_ids.values())

    # Crear la gráfica de barras con Plotly
    fig = go.Figure(data=[go.Bar(x=reaction_ids_list, y=cantidad_list)])

    # Configurar el diseño de la gráfica
    fig.update_layout(
        title="Cantidad de reacciones por tipo",
        xaxis_title="Reaction ID",
        yaxis_title="Cantidad"
    )

    # Mostrar la gráfica en Streamlit
    st.plotly_chart(fig)
    st.markdown("___")
    
    
################ comentarios ######################
if st.sidebar.checkbox('Tabla de comentarios'):
    collection = db['memes_comments']
    registros = collection.find()

    # Crear una lista con los campos "comment" y "objectId"
    data = [["Comentario", "Publicacion", "Usuario"]]
    for registro in registros:
        comment = registro['comment']
        objectId = registro['objectId']
        userId = registro['userId']
        data.append([comment, objectId, userId])

    # Mostrar la tabla en Streamlit
    st.table(data)


#histograma
if st.sidebar.checkbox('Grafica de barras comments'):

    collection = db['memes_comments']
    registros = collection.find()

    # Obtener los "reactionId" y contar la cantidad de cada uno
    reaction_ids = [registro['comment'] for registro in registros]
    contador_reaction_ids = Counter(reaction_ids)

    # Obtener los datos para la gráfica
    reaction_ids_list = list(contador_reaction_ids.keys())
    cantidad_list = list(contador_reaction_ids.values())

    # Crear la gráfica de barras con Plotly
    fig = go.Figure(data=[go.Bar(x=reaction_ids_list, y=cantidad_list)])

    # Configurar el diseño de la gráfica
    fig.update_layout(
        title="Cantidad de comentarios por publicacion",
        xaxis_title="Comment ID",
        yaxis_title="Cantidad"
    )

    # Mostrar la gráfica en Streamlit
    st.plotly_chart(fig)
    st.markdown("___")