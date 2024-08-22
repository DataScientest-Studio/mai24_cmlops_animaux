from PIL import Image
import os
import imagehash
import sys

# Ajouter le chemin absolu de 'src' à sys.path
sys.path.append(os.path.abspath('../../src'))

# Import du fichier de configuration des chemins
import config_manager
from data.data_utils import rep_files_list, create_folder


# Fonction pour récupérer les infos d'une image
def info_img(img_path):
    try:
        # Caractéristiques image
        img = Image.open(img_path)
        dhash_img = imagehash.dhash(img)
        width = img.size[0]
        height = img.size[1]
        format = img.format
        return (True, [str(dhash_img), width, height, format])
    except Exception as e:
        return (False, f"Erreur info image : {e}")


# Fonction de preprocessing d'une image
def prepocessing_img(img_path, img_dest, existing_dhash=[]):
    # Récupération des infos
    infos = info_img(img_path)
    if infos[0]:
        try:
            infos_img = infos[1]
            # Ouverture de l'image
            img = Image.open(img_path)
            # Reformatage si taille non OK
            if infos_img[1] != 224 or infos_img[2] != 224:
                img = img.resize((224, 224))
            # Teste si l'image existe déjà
            if infos_img[0] in existing_dhash:
                infos_img.append(0)
            else:
                img.save(img_dest, format='JPEG')
                infos_img.append(1)
            return (True, infos_img)
        except Exception as e:
            return (False, f"Erreur preprocessing image : {e}")
    else:
        return (False, infos[1])


# Fonction de preprocessing d'un répertoire entier (sous-dossiers inclus)
def preprocessing_rep(repertory, file_types, rep_dest, existing_dhash):
    try:
        files = rep_files_list(repertory, file_types)
        prep_rep_info = []
        source = str(repertory).split('\\')[-1:][0]
        for file in files:
            prep_img_info_def = []
            classe = str(file[1]).split('_')[0].capitalize()
            if classe not in config_manager.CLASSES:
                classe_det = classe
                classe = 'Others'
            else:
                classe_det = classe
            img_path = os.path.join(file[0], file[1])
            folder_dest = os.path.join(rep_dest, classe)
            cf_res = create_folder(folder_dest)
            if cf_res[0]:
                img_name = str(file[1]).split('.')[0].capitalize() + '.jpg'
                img_dest = os.path.join(folder_dest, img_name)
                pi_res = prepocessing_img(img_path, img_dest, existing_dhash)
                if pi_res[0]:
                    prep_img_info = pi_res[1]
                    if prep_img_info[4] == 1:
                        existing_dhash.append(prep_img_info[0])
                        dbl = 0
                    else:
                        dbl = 1
                    prep_img_info_def = [prep_img_info[0], img_name, classe,
                                         classe_det, source]
                    prep_img_info_def.extend(prep_img_info[1:-1])
                    prep_img_info_def.append(dbl)
                    prep_img_info_def.extend(prep_img_info[-1:])
                    prep_rep_info.append(prep_img_info_def)
                else:
                    return (False, f"Erreur preprocessing image : {pi_res[1]}")
            else:
                return (False, f"Erreur crétion dossier : {cf_res[1]}")
        return (True, prep_rep_info)
    except Exception as e:
        return (False, f"Erreur preprocessing : {e}")
