import sys
import os
import logging
import pandas as pd
# Ajouter le chemin absolu de 'src' à sys.path
sys.path.append(os.path.abspath('../../src'))
from data.extract_dataset_init import extract_zip_init
from data.data_utils import remove_folder, folders_list, exist_test
from data.pexels_api import image_save
from data.preprocessing import preprocessing_rep
from data.dataset_integ import dateset_integ
import config_path


# Configuration du logger
filehandler = os.path.join(config_path.LOGS, '01-initial_data_creation.log')

logging.basicConfig(
    level=logging.INFO,  # Niveau de log (DEBUG, INFO, WARNING, ERROR,
    # CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Format
    # du message de log
    handlers=[
        logging.FileHandler(filehandler, encoding='utf-8'),  # Enregistrement
        # des logs
        logging.StreamHandler()  # Affiche les logs dans la console
    ]
)

# Création logger
logger = logging.getLogger(__name__)

# --- Étape 1 : Suppression des dossiers si déjà existants --- #
NUM_STAGE = 1
STAGE_NAME = "Remove existing folders"
logger.info(f">>>>> stage {NUM_STAGE} : {STAGE_NAME} started <<<<<")

reps_to_clean = [config_path.DATA_INIT, config_path.DATA_INTERIM,
                 config_path.DATA_MODEL_TEST, config_path.DATA_MODEL_TRAIN]

for rep_to_clean in reps_to_clean:
    folders = folders_list(rep_to_clean)
    if len(folders) > 0:
        for folder in folders:
            folder_path = os.path.join(rep_to_clean, folder)
            remove = remove_folder(folder_path)
            if remove[0] is False:
                logger.error(remove[1])
                logger.error(f">>>>> stage {NUM_STAGE} : {STAGE_NAME} \
    failed <<<<<\nx=======x\n")
                sys.exit()
            logger.info(remove[1])
    else:
        rep_name = '/'.join(str(rep_to_clean).split('\\')[-1:])
        logger.info(f"Aucun dossier existant dans {rep_name}")

logger.info(f">>>>> stage {NUM_STAGE} : {STAGE_NAME} completed \
<<<<<\nx=======x\n")


# --- Étape 2 : extraction du fchier zip --- #
NUM_STAGE = 2
STAGE_NAME = "Zip extraction"
logger.info(f">>>>> stage {NUM_STAGE} : {STAGE_NAME} started <<<<<")

extract = extract_zip_init(config_path.DATA_INIT_ZIP, config_path.DATA_INIT)
if extract[0]:
    logger.info(extract[1])
else:
    logger.error(extract[1])
    logger.error(f">>>>> stage {NUM_STAGE} : {STAGE_NAME} failed \
<<<<<\nx=======x\n")
    sys.exit()

logger.info(f">>>>> stage {NUM_STAGE} : {STAGE_NAME} completed \
<<<<<\nx=======x\n")


# --- Étape 3 : Téléchargement des images de la classe 'Others' --- #
NUM_STAGE = 3
STAGE_NAME = "Loading external data for 'Others' class"
logger.info(f">>>>> stage {NUM_STAGE} : {STAGE_NAME} started <<<<<")

filename = "DATA_INIT_OTHERS.csv"
classe = 'Others'
file_path = os.path.join(config_path.REFERENCES, filename)
destination = os.path.join(config_path.DATA_INIT, classe)

# Teste si le fichier de référence existe
if exist_test(file_path):
    logger.info(f"Fichier {filename} présent")
else:
    logger.error(f"Fichier {filename} manquant")
    logger.error(f">>>>> stage {NUM_STAGE} : {STAGE_NAME} failed \
<<<<<\nx=======x\n")
    sys.exit()

# Chargement du fichier en DataFrame
others_df = pd.read_csv(file_path, sep=',', header=0, index_col=0)

nb_img = 0
for img in others_df.values:
    action = image_save(img[2], [img[0], img[1]], destination)
    if action[0] is False:
        logger.error(action[1])
        logger.error(f">>>>> stage {NUM_STAGE} : {STAGE_NAME} failed \
<<<<<\nx=======x\n")
        sys.exit()
    else:
        nb_img += action[1]

if nb_img == others_df.shape[0]:
    logger.info(f"{nb_img} images téléchargées")
else:
    logger.warning(f"{others_df.shape[0] - nb_img} non enregistrées")

logger.info(f">>>>> stage {NUM_STAGE} : {STAGE_NAME} completed \
<<<<<\nx=======x\n")


# --- Étape 4 : Preprocessing --- #
NUM_STAGE = 4
STAGE_NAME = "Images preprocessing"
logger.info(f">>>>> stage {NUM_STAGE} : {STAGE_NAME} started <<<<<")

repertory = config_path.DATA_INIT
rep_dest = config_path.DATA_INTERIM

file_types = ['.jpg', '.jpeg']
existing_dhash = []

prep = preprocessing_rep(repertory, file_types, rep_dest, existing_dhash)
if prep[0]:
    try:
        # Passage en DataFrame
        prep_df = pd.DataFrame(prep[1], columns=['dhash', 'img_name',
                                                 'classe', 'classe_det',
                                                 'source', 'width', 'height',
                                                 'format', 'dbl',
                                                 'preprocessing'])
        # Ajout des champs nécessaires à la BDD
        prep_df['wl_mdl_integ'] = prep_df['preprocessing']
        prep_df['mdl_integ'] = 0
        prep_df['train_sel'] = 0
        prep_df['test_sel'] = 0
        # Sauvegarde DataFrame
        prep_df.to_csv(config_path.DB_IMG, sep=',', header=True, index=False)
        nb_img = prep_df.shape[0]
        nb_img_integ = prep_df['preprocessing'].sum()
        logger.info(f"{nb_img} images traitées / {nb_img_integ} images \
pré-processées")
    except Exception as e:
        logger.error(f"Une erreur est survenue : {e}")
else:
    logger.error(prep[1])
    logger.error(f">>>>> stage {NUM_STAGE} : {STAGE_NAME} failed \
<<<<<\nx=======x\n")
    sys.exit()

logger.info(f">>>>> stage {NUM_STAGE} : {STAGE_NAME} completed \
<<<<<\nx=======x\n")


# --- Étape 5 : Intégration des données au Dataset du modèle --- #
NUM_STAGE = 5
STAGE_NAME = "Images model integration"
logger.info(f">>>>> stage {NUM_STAGE} : {STAGE_NAME} started <<<<<")

integ = dateset_integ()
if integ[0]:
    logger.info(integ[1])
else:
    logger.error(integ[1])
    logger.error(f">>>>> stage {NUM_STAGE} : {STAGE_NAME} failed \
<<<<<\nx=======x\n")
    sys.exit()

logger.info(f">>>>> stage {NUM_STAGE} : {STAGE_NAME} completed \
<<<<<\nx=======x\n")
