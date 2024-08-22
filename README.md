Animal recognition
==============================

This project is a starting Pack for MLOps projects based on the subject "Animal recognition". It's not perfect so feel free to make some modifications on it.

Project Organization
------------

    ├── LICENSE
    ├── README.md                   <- The top-level README for developers using this project.
    ├── data
    │   ├── 1. Initial              <- The original, immutable data dump.
    |   ├── 2. External             <- New data Collection (Production)
    │   ├── 3. interim              <- Intermediate data that has been transformed and waiting model
    |   |                              integration
    │   ├── 4. processed            <- The final, canonical data sets for modeling.
    │
    ├── logs                        <- Logs from pipelines
    │
    ├── models                      <- Trained and serialized models, model predictions, or model
    |                                   summaries
    │
    ├── notebooks                   <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                               the creator's initials, and a short `-` delimited description, e.g.
    │                               `1.0-jqp-initial-data-exploration`.
    │
    ├── references                  <- Data dictionaries, manuals, and all other explanatory materials.
    |   ├── DATA_INIT_OTHERS.csv    <- URLs to download "Others" classe for initial dataset
    │   |── DATA_INIT.zip           <- Initial data
    |                                  https://www.kaggle.com/datasets/likhon148/animal-data
    |
    ├── reports                     <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures                 <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt            <- The requirements file for reproducing the analysis environment
    |                                  (except train_model -> cf. requirements_dl.txt)
    │
    ├── src                         <- Source code for use in this project.
    │   ├── __init__.py             <- Makes src a Python module
    │   │
    │   ├── data                    <- Scripts to download and generate data
    │   │   ├── __init__.py
    |   |   ├── 01-initial_data_creation.py <- Pipeline for dataset init creation
    |   |   ├── 03-TU_data.py               <- Unit tests for data
    │   │   ├── data_utils.py               <- Usefull fonctions for data (eg. create folder, ...)
    │   │   ├── extract_dataset_init.py     <- To extract DATA_INIT.zip to data/1. Initial
    |   |   ├── pexels_api.py               <- Api to download pictures from https://www.pexels.com
    │   │   └── preprocessing.py            <- Pictures preprocessing
    |   |
    │   ├── models                  <- Scripts to train models and then use trained models to make
    │   │   │                          predictions
    │   │   ├── 
    │   │   └── 
    |   |
    │   ├── visualization           <- Scripts to create exploratory and results oriented visualizations
    │   │   └── 
    |   |
    |   ├── .env.exemple            <- Environnement variables (to rename .env)
    │   ├── config_manager.py
    |   └── config_path.py

---------

## Steps to follow 

Convention : All python scripts must be run from the root specifying the relative file path.

### 1- Create a virtual environment using Virtualenv.

    `python -m venv my_env`

###   Activate it 

    `./my_env/Scripts/activate`

###   Install the packages from requirements.txt

    `pip install -r .\requirements.txt`

### 2- Execute '01-initial_data_creation' to create the initial dataset.

    `cd .\src\data'
    `python 01-initial_data_creation.py` ### 1 file log (./logs) and 1 file csv (./references) whith the informations of database_images are created

### 3- Execute the unit tests to control if initial dataset creation is right.
    'python -m pytest 03-TU_data.py 




### Old project - Datascientest example
### 3- Execute make_dataset.py initializing `./data/raw` as input file path and `./data/preprocessed` as output file path.

    `python .\src\data\make_dataset.py`

### 4- Execute train_model.py to instanciate the model in joblib format

    `python .\src\models\train_model.py`

### 5- Finally, execute predict_model.py with respect to one of these rules :
  
  - Provide a json file as follow : 

    
    `python ./src/models/predict_model.py ./src/models/test_features.json`

  test_features.json is an example that you can try 

  - If you do not specify a json file, you will be asked to enter manually each feature. 


------------------------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
