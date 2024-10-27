import streamlit as st
import sys
import os
sys.path.append(os.path.abspath('../../src/config'))
# Import du fichier de configuration des chemins
import config_path

sous_menu = ["Architecture", "Base de données", "Modèle", "Stack MLOps"]


def run():
    banner_path = os.path.join(config_path.APP_ASSETS, "banners",
                               "presentation_banner.jpg")
    st.image(banner_path)
    with st.sidebar:
        st.title("")
        st.header("Presentation")
        choix = st.radio("Sous menu",
                         sous_menu,
                         label_visibility='hidden')

    if choix == sous_menu[sous_menu.index("Architecture")]:
        st.title(choix)
        st.image("../../references/architecture.jpg")

    elif choix == sous_menu[sous_menu.index("Base de données")]:
        st.title(choix)
        st.markdown("---")
        on_display_db_init = st.toggle("Initialisation base de données",
                                       key="db_init")
        if on_display_db_init:
            st.image("../../references/00-initial_data_creation.jpg")
        st.markdown("""  """)

        on_display_db_ingest = st.toggle("Ingestion nouvelles images",
                                         key="db_ingest")
        if on_display_db_ingest:
            st.image("../../references/00-initial_data_creation.jpg")

    elif choix == sous_menu[sous_menu.index("Modèle")]:
        st.title(choix)
        st.markdown("---")
        st.markdown(
            """
            Modèle blablabla
            """)
        st.markdown("""  """)

    elif choix == sous_menu[sous_menu.index("Stack MLOps")]:
        st.title(choix)
        st.markdown("---")
        st.markdown(
            """
            Stack MLOps blablabla
            """)
        st.markdown("""  """)
