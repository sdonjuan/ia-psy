import streamlit as st
import random
from datetime import datetime

# Configuration de l'application
st.set_page_config(
    page_title="Écoute - Compagnon Emotionnel",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé
st.markdown("""
<style>
    .stTextArea [data-baseweb=textarea] {
        background-color: #f8f9fa;
        border-radius: 15px;
    }
    .stButton>button {
        background-color: #4a6fa5;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
    }
    .st-emotion-cache-1y4p8pa {
        padding: 2rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Données des émotions (version complète)
EMOTIONS_DATA = {
    "tristesse": {
        "mots_cles": ["tristesse", "triste", "déprimé", "déprimée", "déprime", "chagrin"],
        "reponses": [
            "Je ressens une profonde tristesse dans tes mots. Cette émotion est lourde à porter, mais tu n'es pas seul(e).",
            "Ton chagrin mérite d'être entendu. Prends tout le temps qu'il te faut.",
            "La tristesse que tu décris montre à quel point cette situation compte pour toi."
        ],
        "exercices": [
            "Écris une lettre à ta tristesse comme si c'était une personne. Que voudrais-tu lui dire ?",
            "Essaie le 'bain de forêt' : marche lentement en imaginant que la nature absorbe ta peine."
        ],
        "citations": [
            "« Les larmes sont les mots que le cœur ne peut exprimer. » - John Locke"
        ]
    },
    "anxiété": {
        "mots_cles": ["stress", "anxiété", "angoissé", "panique", "inquiet"],
        "reponses": [
            "Je sens ton anxiété à travers tes mots. Prenons une grande respiration ensemble.",
            "Ton esprit semble pris dans une tempête. Concentrons-nous sur l'ici et maintenant."
        ],
        "exercices": [
            "Technique 5-4-3-2-1 : Nomme 5 choses que tu vois, 4 que tu touches, 3 que tu entends, 2 que tu sens, 1 que tu goûtes.",
            "Respiration carrée : Inspire 4s → Retiens 4s → Expire 4s → Pause 4s. Répète 5 fois."
        ],
        "citations": [
            "« L'anxiété est comme une chaise berçante : elle te donne quelque chose à faire, mais ne t'avance pas. » - Jodi Picoult"
        ]
    }
    # (Toutes les autres émotions avec la même structure)
}

# Fonctions clés
def detect_emotion(text):
    text = text.lower()
    for emotion, data in EMOTIONS_DATA.items():
        if any(keyword in text for keyword in data["mots_cles"]):
            return emotion
    return None

def generate_response(emotion=None):
    if emotion:
        data = EMOTIONS_DATA[emotion]
        return {
            "reponse": random.choice(data["reponses"]),
            "exercice": random.choice(data["exercices"]),
            "citation": random.choice(data["citations"])
        }
    else:
        generic = [
            "Je t'écoute avec attention. Dis-m'en plus si tu le souhaites.",
            "Merci de partager cela. Comment te sens-tu en ce moment précis ?",
            "Prends une profonde respiration. Je suis là pour t'accompagner."
        ]
        return {"reponse": random.choice(generic)}

# Interface utilisateur
st.title("🌱 Écoute Emotionnelle")
st.subheader("Un espace sûr pour explorer tes émotions")

with st.expander("💡 Conseils pour utiliser cet outil"):
    st.write("""
    - Exprime-toi librement, comme si tu parlais à un ami bienveillant
    - Utilise des mots simples pour décrire ce que tu ressens
    - Reviens autant de fois que nécessaire
    """)

# Historique de conversation
if "history" not in st.session_state:
    st.session_state.history = []

# Interaction principale
user_input = st.text_area(
    "Parle-moi de ce que tu ressens aujourd'hui...",
    height=150,
    key="input",
    help="Décris tes émotions avec tes propres mots"
)

col1, col2 = st.columns([1, 3])
with col1:
    if st.button("Envoyer", type="primary"):
        if user_input.strip():
            # Traitement du message
            emotion = detect_emotion(user_input)
            response = generate_response(emotion)
            
            # Enregistrement dans l'historique
            timestamp = datetime.now().strftime("%H:%M")
            st.session_state.history.append({
                "time": timestamp,
                "user": user_input,
                "bot": response,
                "emotion": emotion
            })
            
            # Affichage de la réponse
            st.session_state.last_response = response
            st.session_state.show_response = True
        else:
            st.warning("Écris quelque chose pour que je puisse te répondre")

with col2:
    if st.button("Nouvelle conversation", help="Recommencer à zéro"):
        st.session_state.history = []
        st.session_state.show_response = False
        st.experimental_rerun()

# Affichage des réponses
if st.session_state.get("show_response", False):
    response = st.session_state.last_response
    
    st.markdown("---")
    st.markdown(f"**💬 Réponse :**  \n{response['reponse']}")
    
    if 'exercice' in response:
        with st.expander("🛠 Exercice pour toi"):
            st.write(response['exercice'])
    
    if 'citation' in response:
        st.caption(f"✨ *{response['citation']}*")

# Historique des conversations
if st.session_state.history:
    st.markdown("---")
    st.subheader("Ton historique")
    for i, exchange in enumerate(reversed(st.session_state.history[-5:])):
        with st.expander(f"📝 Conversation à {exchange['time']}"):
            st.markdown(f"**Toi :**  \n{exchange['user']}")
            st.markdown(f"**Réponse :**  \n{exchange['bot']['reponse']}")
            if exchange['emotion']:
                st.caption(f"Détecté : {exchange['emotion'].capitalize()}")

# Pied de page
st.markdown("---")
st.caption("""
ℹ️ Cet outil ne remplace pas un professionnel de santé.  
En cas de détresse, contacte le [3114](https://www.3114.fr) (France) ou ton médecin.
""")
