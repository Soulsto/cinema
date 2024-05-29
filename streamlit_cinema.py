import streamlit as st
import pandas as pd
from unidecode import unidecode
import yaml
from yaml.loader import SafeLoader
import os
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

# Spécifiez le chemin absolu du fichier config.yaml
config_path = 'C:/Users/Admin/Documents/pop_data/config.yaml'

# Charger la configuration
if os.path.exists(config_path):x
    with open(config_path) as file:
        config = yaml.load(file, Loader=SafeLoader)
else:
    st.error(f"Le fichier config.yaml est introuvable à l'emplacement : {config_path}")

# Fonction simple pour vérifier les identifiants
def check_credentials(email, password):
    for user, info in config['credentials']['usernames'].items():
        if info['email'] == email and info['password'] == password:
            return info['name']
    return None

# Fonction pour afficher la page principale
def main_page():
    # Lire le fichier CSV
    df = pd.read_csv("df_test.csv", sep=',')

    # Créer une nouvelle colonne avec les noms en minuscules et sans accents
    df['primaryNameLower'] = df['primaryName'].apply(lambda x: ', '.join([unidecode(name.lower()) for name in x.split(', ')]))

    # Vérifier et corriger les valeurs de `poster_path_test`
    default_image_path = 'C:/Users/Admin/Documents/pop_data/img_film_manqu.jpg'  
    df['poster_path_test'] = df['poster_path_test'].apply(lambda x: x if isinstance(x, str) else default_image_path)

    # CSS pour assurer un fond noir et styliser les boutons et les champs de texte
    st.markdown(
        """
        <style>
        .block-container {
            background-color: black !important;
            color: #FFC300 !important;
            width: 100% !important;
            padding: 0 !important;
        }
        .main .block-container {
            padding: 1rem !important;
            width: calc(100% - 2rem) !important;
        }
        .st-emotion-cache-13ln4jf {
            max-width: none !important; /* Remove max-width limitation */
        }
        body {
            background-color: black !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        .header {
            background-color: black !important;
            padding: 10px;
            text-align: center;
            width: 100%;
            top: 0;
            left: 0;
        }
        textarea {
            min-height: 196px !important;
        }
        .yellow-text {
            color: #FFC300 !important;
        }
        .stTextInput > div > div > input {
            color: black !important;
            background-color: white !important;
        }
        .stTextInput input::placeholder {
            color: black !important; /* Placeholder text color */
        }
        .content {
            background-color: black !important;
            color: #FFC300 !important;
            width: 100% !important;
        }
        .stImage > div {
            background-color: black !important;
            width: 100% !important;
        }
        .stImage img {
            background-color: black !important;
        }
        .stButton button {
            background-color: black !important;
            border: 2px solid yellow !important;
            color: #FFC300 !important;
        }
        .button-row {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #FFC300 !important; /* Title colors */
        }
        .stTextInput {
            margin: auto;
        }
        .stTextInput label {
            color: #FFC300 !important;
        }
        h1 {
            color: #FFC300 !important;
        }
        .stColumns {
            margin-bottom: 20px !important;
        }
        .stImage, .stMarkdown {
            display: flex;
            align-items: center.
        }
        .film-row {
            margin-bottom: 40px !important; /* Ajouter de l'espace entre les lignes de films */
        }
        .result-title {
            font-size: 24px !important;
            font-weight: bold !important.
        }
        .film-title {
            font-size: 20px !important.
            font-weight: bold !important.
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Contenu de l'application
    st.markdown('<div class="content">', unsafe_allow_html=True)

    # En-tête avec l'image
    st.image("famille.jpg", use_column_width=True)
    st.title("Bienvenue ! ")
    st.title("Quel film allez-vous trouver aujourd'hui ?")
    st.text("")
    st.text("")
    st.text("")
    st.header("Faites une recherche par nom :")

    # Input de l'utilisateur
    if 'name' not in st.session_state:
        st.session_state.name = ''

    def clear_text():
        st.session_state.name = ''
        st.session_state.num_movies = num_movies_to_display

    # Définir les colonnes
    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])

    # Ajouter un input de texte dans la première colonne plus petite
    with col1:
        name = st.text_input(label="", placeholder="Entrez un nom d'actrice, acteur, réalisatrice, compositeur (...)", value=st.session_state.name, key='name')

    # Convertir le texte en minuscules et retirer les accents
    name2 = unidecode(name.lower())

    num_movies_to_display = 4

    # Filtrer le DataFrame en fonction de l'entrée de l'utilisateur
    if name:
        filtered_df = df[df["primaryNameLower"].str.contains(name2, case=False, na=False)]
        filtered_df = filtered_df.sort_values(by="averageRating", ascending=False)
        
        # Utiliser session state pour gérer la pagination
        if 'num_movies' not in st.session_state:
            st.session_state.num_movies = num_movies_to_display

        movies_to_show = filtered_df.head(st.session_state.num_movies)

        if not movies_to_show.empty:
            st.markdown(f"<div class='result-title'>Résultats pour '{name}':</div>", unsafe_allow_html=True)

            # Afficher les films en 4 colonnes (2 colonnes pour images et 2 colonnes pour descriptions)
            for i in range(0, len(movies_to_show), 2):
                cols = st.columns([1, 2, 1, 2], gap="large")
                for j, (_, row) in enumerate(movies_to_show.iloc[i:i+2].iterrows()):
                    with cols[j * 2]:
                        st.image(row["poster_path_test"], width=200)
                    with cols[j * 2 + 1]:
                        st.markdown(f"<div class='film-title'>{row['originalTitle'].upper()}</div>", unsafe_allow_html=True)
                        st.write(f"**Descriptif:** {row['overview']}")
                st.markdown("<div class='film-row'></div>", unsafe_allow_html=True)  # Ajouter de l'espace entre les lignes de films

            st.markdown('<div class="button-row">', unsafe_allow_html=True)
            if st.button('Voir plus', key='see_more'):
                st.session_state.num_movies += num_movies_to_display
                st.experimental_rerun()
            if st.button('Voir moins', key='see_less'):
                if st.session_state.num_movies > num_movies_to_display:
                    st.session_state.num_movies -= num_movies_to_display
                    st.experimental_rerun()
            if st.button('Rafraîchir', on_click=clear_text, key='refresh'):
                st.experimental_rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.write(f"Aucun film trouvé pour '{name}'")

    else:
        # Ajouter un espace de remplissage pour maintenir le fond noir
        st.markdown("<div style='height: 500px;'></div>", unsafe_allow_html=True)
        # Close the div
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("Recherche de films similaires")

    if 'titre' not in st.session_state:
        st.session_state.titre = ''

    def clear_text2():
        st.session_state.titre = ''

    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])

    with col1:
        titre = st.text_input("Entrez un titre de film:", value=st.session_state.titre, key='titre')

    titre = unidecode(titre)

    if titre:
        var_exp = ['startYear', 'runtimeMinutes', 'averageRating', 'numVotes', 'Action', 'Drama', 'Fantasy']
        X = df[var_exp]

        # Normalisation des données
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Initialisation du modèle KNN
        knn = NearestNeighbors(n_neighbors=5, metric='euclidean')
        knn.fit(X_scaled)

        def films_semblables(titre, df, knn, scaler):
            film_input = df[df['originalTitle'].str.contains(titre, case=False, na=False)] #nom du film renseigné par l'utilisateur
            if film_input.empty:
                return ["Titre non trouvé"]
            
            # Utiliser le premier résultat correspondant
            indice = film_input.index[0] #trouver l'indice du film renseigné par l'utilisateur
            val_films = X.iloc[indice].values.reshape(1, -1) #on prend les valeurs de la ligne et on met en array
            val_films_scaled = scaler.transform(val_films)
            distances, indices = knn.kneighbors(val_films_scaled)
            similar_indices = indices[0]  # Utiliser les indices retournés sans les aplatir
            return df.iloc[similar_indices[1:]]  # Exclure le film lui-même

        resultat = films_semblables(titre, df, knn, scaler)
        
        if isinstance(resultat, list) and resultat[0] == "Titre non trouvé":
            st.write(resultat[0])
        else:
            st.write("Films similaires :")
            for i in range(0, len(resultat), 2):
                cols = st.columns([1, 2, 1, 2], gap="large")
                for j, (_, row) in enumerate(resultat.iloc[i:i+2].iterrows()):
                    with cols[j * 2]:
                        st.image(row["poster_path_test"], width=200)
                    with cols[j * 2 + 1]:
                        st.markdown(f"<div class='film-title'>{row['originalTitle'].upper()}</div>", unsafe_allow_html=True)
                        st.write(f"**Descriptif:** {row['overview']}")
                st.markdown("<div class='film-row'></div>", unsafe_allow_html=True)  # Ajouter de l'espace entre les lignes de films

            st.markdown('<div class="button-row">', unsafe_allow_html=True)
            if st.button('Rafraîchir', on_click=clear_text2, key='refresh_similar'):
                st.experimental_rerun()

# Interface de connexion
def login_page():
    st.markdown(
        """
        <style>
        .block-container {
            background-color: black !important;
            color: #FFC300 !important;
            width: 100% !important;
            padding: 0 !important;
        }
        .main .block-container {
            padding: 1rem !important;
            width: calc(100% - 2rem) !important;
        }
        .st-emotion-cache-13ln4jf {
            max-width: none !important; /* Remove max-width limitation */
        }
        body {
            background-color: black !important;
            margin: 0 !important;
            padding: 0 !important.
        }
        .header {
            background-color: black !important;
            padding: 10px.
            text-align: center.
            width: 100%.
            top: 0.
            left: 0.
        }
        textarea {
            min-height: 196px !important.
        }
        .yellow-text {
            color: #FFC300 !important.
        }
        .stTextInput > div > div > input {
            color: black !important.
            background-color: white !important.
        }
        .stTextInput input::placeholder {
            color: black !important; /* Placeholder text color */
        }
        .content {
            background-color: black !important.
            color: #FFC300 !important.
            width: 100% !important.
        }
        .stImage > div {
            background-color: black !important.
            width: 100% !important.
        }
        .stImage img {
            background-color: black !important.
        }
        .stButton button {
            background-color: black !important.
            border: 2px solid #FFC300 !important.
            color: #FFC300 !important.
        }
        .button-row {
            display: flex.
            justify-content: center.
            gap: 10px.
            margin-top: 20px.
        }
        h1, h2, h3, h4, h5, h6 {
            color: #FFC300 !important; /* Title colors */
        }
        .stTextInput {
            margin: auto.
        }
        .stTextInput label {
            color: #FFC300 !important.
        }
        h1 {
            color: #FFC300 !important.
        }
        .stColumns {
            margin-bottom: 20px !important.
        }
        .stImage, .stMarkdown {
            display: flex.
            align-items: center.
        }
        .film-row {
            margin-bottom: 40px !important; /* Ajouter de l'espace entre les lignes de films */
        }
        .result-title {
            font-size: 24px !important.
            font-weight: bold !important.
        }
        .film-title {
            font-size: 20px !important.
            font-weight: bold !important.
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Contenu de l'application
    st.markdown('<div class="content">', unsafe_allow_html=True)

    # En-tête avec l'image
    st.image("famille.jpg", use_column_width=True)
    st.title("Ciné Creuse recommandations")
    st.title("")
    st.text("")
    st.text("")
    st.text("")
    st.header("Connexion")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
        
        with col1:
            email = st.text_input("Email")
            password = st.text_input("Mot de passe", type="password")
            if st.button("Se connecter"):
                user_name = check_credentials(email, password)
                if user_name:
                    st.session_state.logged_in = True
                    st.session_state.user_name = user_name
                    st.experimental_rerun()  # Redémarrer l'application pour charger la nouvelle page
                else:
                    st.error("Identifiants incorrects")
    else:
        main_page()

# Afficher la page de connexion ou la page principale en fonction de l'état de connexion
if st.session_state.get('logged_in'):
    main_page()
else:
    login_page()