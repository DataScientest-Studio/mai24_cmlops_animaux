import streamlit as st
import os
import sys
sys.path.append(os.path.abspath('../../src/config'))
# Import du fichier de configuration des chemins
import config_path

title = "Évolutions / Améliorations"


def run():
    banner_path = os.path.join(config_path.APP_ASSETS, "banners",
                               "evol_banner.jpg")
    st.image(banner_path)

    st.title(title)

    st.markdown("---")

    st.markdown(
        """
        ### Fonctionnalités :\n
        >- monitoring
        >- traitement d'images (détourage, palette couleur, ...)
        >- interprétabilité modèle (GradCam)\n

        ### Évolutions :\n
        >- Passage json->mongoDB pour la gestion de la base documents
        >- Déployer sur une architecture cloud

        """
    )