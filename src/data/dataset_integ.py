import os
import sys
import pandas as pd
import numpy as np
# Ajouter le chemin absolu de 'src' à sys.path
sys.path.append(os.path.abspath('../src'))

# Import du fichier de configuration des chemins
import config_path
import config_manager
from data.data_utils import cp_file, remove_file


# Fonction tirage alétoire à partir d'une liste
def list_random_sel(source_list, seed, nb_sel):
    # Teste si nombre de lignes à sélectionner est inférieur à la taille de la\
    # liste
    if nb_sel <= len(source_list):
        try:
            sortie = []
            np.random.seed(seed)
            sel = np.random.choice(source_list, size=nb_sel, replace=False)
            sortie.extend([int(x) for x in sel])
            return (True, sortie)
        except Exception as e:
            return (False, f"Une erreur est survenue : {e}")
    else:
        return (False, "Taille de la liste insuffisante")


# Fonction pour intégrer des données au dataset
def dateset_integ(classes=config_manager.CLASSES,
                  train_weight=config_manager.TRAIN_WEIGHT,
                  seed=config_manager.SEED,
                  integration_min=config_manager.INTEGRATION_MIN):
    try:
        # Ouverture de la base image
        df_img_info = pd.read_csv(config_path.DB_IMG, sep=',', header=0)
        # Images ayant été précessossées mais encore non intégré au dataset
        df_img_ds = df_img_info[(df_img_info['preprocessing'] == 1) &
                                (df_img_info['mdl_integ'] == 0)]
        # Calcul du nombre d'images à sélectionner par classe
        nb_img_sel = int(df_img_ds.groupby('classe')['wl_mdl_integ']
                         .sum().min())
        # Teste si le nombre minimal est atteint
        if nb_img_sel < integration_min:
            return (False, f"Le nombre minimal d'images ({integration_min}) \
par classe n'est pas atteint")

        # Tirage aléatoire
        img_mdl_sel, img_train_sel = [], []
        for classe in classes:
            base_sel = list(df_img_ds[df_img_ds['classe'] == classe].index)
            # Sélection des images pour le modèle
            img_mdl = list_random_sel(base_sel, seed, nb_img_sel)
            if img_mdl[0]:
                img_mdl_sel.extend(img_mdl[1])
            else:
                return (False, f"Erreur lors de la sélection pour modèle : \
{img_mdl[1]}")
            # Sélection des images pour le train
            nb_img_train_sel = int(nb_img_sel * train_weight)
            img_train = list_random_sel(img_mdl[1], seed, nb_img_train_sel)
            if img_train[0]:
                img_train_sel.extend(img_train[1])
            else:
                return (False, f"Erreur lors de la sélection pour train : \
{img_train[1]}")
        # Copie les fichiers et les supprime du dossier "3. Interim"
        nb_img_integ = 0
        for index in img_mdl_sel:
            classe = df_img_info.loc[index, 'classe']
            img_name = df_img_info.loc[index, 'img_name']
            file_path = os.path.join(config_path.DATA_INTERIM, classe,
                                     img_name)
            train = 0
            if index in img_train_sel:
                file_dest = os.path.join(config_path.DATA_MODEL_TRAIN, classe,
                                         img_name)
                train = 1
            else:
                file_dest = os.path.join(config_path.DATA_MODEL_TEST, classe,
                                         img_name)
            # Copie le fichier
            cp = cp_file(file_path, file_dest)
            if cp[0]:
                nb_img_integ += 1
                # Mise à jour Dataframe
                df_img_info.loc[index, 'mdl_integ'] = 1
                if train == 1:
                    df_img_info.loc[index, 'train_sel'] = 1
                else:
                    df_img_info.loc[index, 'test_sel'] = 1
            else:
                print(file_path, file_dest)
                df_img_info.to_csv(config_path.DB_IMG, sep=',', header=True,
                                   index=False)
                return (False, f"Erreur copie fichier : {cp[1]}")
            # Supprime le fichier
            rmv = remove_file(file_path)
            if rmv[0]:
                # Mise à jour Dataframe
                df_img_info.loc[index, 'wl_mdl_integ'] = 0
            else:
                df_img_info.to_csv(config_path.DB_IMG, sep=',', header=True,
                                   index=False)
                return (False, f"Erreur suppression fichier : {rmv[1]}")
        # Sauvegarde de la base images mise à jour
        df_img_info.to_csv(config_path.DB_IMG, sep=',', header=True,
                           index=False)
        # Retourne stats :
        nb_img_waiting = df_img_info['wl_mdl_integ'].sum()
        return (True, f"{nb_img_integ} images intégrées (soit {nb_img_sel} \
par classe). {nb_img_waiting} images encore en attente d'intégration.")
    except Exception as e:
        return (False, f"Une erreur est survenue : {e}")
