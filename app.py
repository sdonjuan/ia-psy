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
""")import streamlit as st
import random
from datetime import datetime
import base64

# ====================== #
#    CONFIGURATION UI    #
# ====================== #
def setup_ui():
    """Configuration cosmétique avancée"""
    st.set_page_config(
        page_title="Serena - Compagnon Émotionnel IA",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Injection CSS personnalisé
    st.markdown(f"""
    <style>
        /* Fond d'écran subtil */
        .stApp {{
            background-image: url("data:image/svg+xml;base64,{base64.b64encode(open('background.svg', 'rb').read()).decode()}");
            background-attachment: fixed;
            background-size: cover;
        }}
        
        /* Cartes de conversation */
        .message-user {{
            background: linear-gradient(135deg, #6e8efb 0%, #a777e3 100%);
            color: white;
            border-radius: 18px 18px 0 18px;
            padding: 12px 16px;
            margin: 8px 0;
            max-width: 80%;
            margin-left: auto;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .message-ai {{
            background: #ffffff;
            color: #333;
            border-radius: 18px 18px 18px 0;
            padding: 12px 16px;
            margin: 8px 0;
            max-width: 80%;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid #eee;
        }}
        
        /* Zone de texte améliorée */
        .stTextArea textarea {{
            border-radius: 20px !important;
            padding: 16px !important;
            font-size: 16px !important;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        /* Boutons modernes */
        .stButton>button {{
            border-radius: 20px !important;
            padding: 10px 24px !important;
            background: linear-gradient(135deg, #6e8efb 0%, #a777e3 100%) !important;
            color: white !important;
            border: none !important;
            font-weight: 500 !important;
            transition: all 0.3s !important;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(106, 115, 247, 0.3) !important;
        }}
        
        /* En-tête élégant */
        .header {{
            font-family: 'Segoe UI', sans-serif;
            text-align: center;
            margin-bottom: 2rem;
        }}
        
        .title {{
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #6e8efb 0%, #a777e3 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        
        .subtitle {{
            color: #666;
            font-weight: 400;
            font-size: 1.1rem;
        }}
    </style>
    """, unsafe_allow_html=True)

# ====================== #
#      CORE FUNCTION     #
# ====================== #
def render_message(role, content):
    """Affiche un message stylisé"""
    if role == "user":
        st.markdown(f'<div class="message-user">{content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="message-ai">{content}</div>', unsafe_allow_html=True)

# ====================== #
#       APPLICATION      #
# ====================== #
def main():
    setup_ui()
    
    # En-tête élégant
    st.markdown("""
    <div class="header">
        <div class="title">Serena</div>
        <div class="subtitle">Votre compagnon émotionnel intelligent</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Colonnes pour une mise en page équilibrée
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("mindfulness.png", width=150)
        st.caption("💡 Parlez librement comme à un ami bienveillant")
        
        with st.expander("📚 Ressources utiles"):
            st.markdown("""
            - **Urgence France** : 3114  
            - **Écoute anonyme** : 0800 23 13 13  
            - [Trouver un psy](https://annuaire.sante.fr)
            """)
    
    with col2:
        # Historique de conversation
        if "history" not in st.session_state:
            st.session_state.history = []
            
        # Affichage des messages
        chat_placeholder = st.empty()
        
        with chat_placeholder.container():
            for msg in st.session_state.history[-6:]:
                render_message(msg["role"], msg["content"])
                
                # Affichage conditionnel des exercices
                if msg.get("exercise"):
                    with st.expander("💡 Exercice suggéré"):
                        st.markdown(f"✨ *{msg['exercise']}*")
        
        # Zone de saisie moderne
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area("Votre message...", height=100, key="input")
            
            cols = st.columns([3, 1])
            with cols[0]:
                if st.form_submit_button("Envoyer", use_container_width=True):
                    if user_input.strip():
                        # Simulation réponse IA
                        ai_response = generate_ai_response(user_input)
                        
                        # Ajout à l'historique
                        timestamp = datetime.now().strftime("%H:%M")
                        st.session_state.history.append({
                            "role": "user",
                            "content": user_input,
                            "time": timestamp
                        })
                        
                        st.session_state.history.append({
                            "role": "ai",
                            "content": ai_response["text"],
                            "exercise": ai_response.get("exercise"),
                            "time": timestamp
                        })
                        
                        st.experimental_rerun()
            
            with cols[1]:
                if st.form_submit_button("Effacer", type="secondary", use_container_width=True):
                    st.session_state.history = []
                    st.experimental_rerun()

def generate_ai_response(user_input):
    """Génère une réponse contextuelle (à remplacer par votre logique)"""
    responses = {
        "triste": {
            "text": "Je ressens une profonde tristesse dans vos mots. Cette émotion est valide et mérite d'être entendue.",
            "exercise": "Essayez l'écriture expressive : décrivez votre tristesse comme si c'était un paysage (couleur, forme, texture)."
        },
        # ... autres scénarios
    }
    
    # Détection simplifiée (à améliorer)
    if "triste" in user_input.lower():
        return responses["triste"]
    else:
        return {
            "text": "Je vous écoute avec attention. Pouvez-vous en dire plus sur ce que vous ressentez ?",
            "exercise": None
        }

if __name__ == "__main__":
    main() 
    from streamlit_lottie import st_lottie
import json

# Charger une animation Lottie
with open("animation.json") as f:
    lottie_anim = json.load(f)
    
st_lottie(lottie_anim, height=200)
# Ajouter ce CSS
.dark-mode {
    background-color: #1e1e1e !important;
    color: #f0f0f0 !important;
}

