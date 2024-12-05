import streamlit as st
from datetime import datetime, timedelta
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu

# Constantes
SESSION_DURATION = 30  # Durée de la session en minutes

# Fonction : Initialiser la session
def initialize_session():
    st.session_state.start_time = datetime.now()
    st.session_state.is_authenticated = True
    st.session_state.current_page = "Accueil"  # Page par défaut

# Vérification et initialisation de la session
if 'start_time' not in st.session_state or 'is_authenticated' not in st.session_state:
    initialize_session()

# Authentification
user_data = {
    'usernames': {
        'utilisateur': {
            'name': 'utilisateur',
            'password': 'utilisateurMDP',
            'email': 'utilisateur@gmail.com',
            'failed_login_attempts': 0,
            'logged_in': False,
            'role': 'utilisateur',
        },
        'root': {
            'name': 'root',
            'password': 'rootMDP',
            'email': 'admin@gmail.com',
            'failed_login_attempts': 0,
            'logged_in': False,
            'role': 'administrateur',
        }
    }
}

authenticator = Authenticate(
    user_data,             # Données des comptes
    "cookie_name",         # Nom du cookie
    "cookie_key",          # Clé du cookie
    30                     # Expiration du cookie (jours)
)

authenticator.login()

# Fonction : Page d'accueil
def accueil():
    st.markdown("<h1 style='text-align: center;'>Bienvenue sur ma page</h1>", unsafe_allow_html=True)
    st.image("bienvenue-sur-ma-page.jpg")

# Fonction : Page des photos
def photos():
    st.markdown("<h1 style='text-align: center;'>Album Photo</h1>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("sangoku.gif", caption="Goku", use_container_width=True)
        #st.header("A cat")
        #st.image("https://static.streamlit.io/examples/cat.jpg")

    with col2:
        st.image("sangohan.gif", caption="Gohan", use_container_width=True)
        #st.header("A dog")
        #st.image("https://static.streamlit.io/examples/dog.jpg")

    with col3:
        st.image("goten.gif", caption="Goten", use_container_width=True)
        #st.header("An owl")
        #st.image("https://static.streamlit.io/examples/owl.jpg")

    with col4:
        st.image("pan.gif", caption="Pan", use_container_width=True)
  

# Interface utilisateur
if st.session_state["authentication_status"]:
    # Affichage du message de durée de session uniquement après connexion réussie
    if "session_message_displayed" not in st.session_state:
        st.session_state.session_message_displayed = True
        st.success(f"Vous êtes connecté pour {SESSION_DURATION} minutes.\n\nTemps restant : {SESSION_DURATION:.0f} minutes.")
    
    # Menu de navigation dans la barre latérale
    with st.sidebar:
        authenticator.logout("Déconnexion")
        st.markdown('Bienvenue, _root_')
        # Menu latéral
        selection = option_menu(
            menu_title=None,
            options=["Accueil", "Photos"],
            icons=["house", "camera"],
            default_index=0
        )
        # Met à jour la page courante dans la session
        st.session_state.current_page = selection

    # Affiche la page sélectionnée
    if st.session_state.current_page == "Accueil":
        accueil()

    elif st.session_state.current_page == "Photos":
        photos()

elif st.session_state["authentication_status"] is False:
    st.error("L'username ou le mot de passe est incorrect.")
elif st.session_state["authentication_status"] is None:
    st.warning("Les champs username et mot de passe doivent être remplis.")
