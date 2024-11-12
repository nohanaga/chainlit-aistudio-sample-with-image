# chainlit-aistudio-sample

## Install
`pip install -r requirements.txt`

## Settings
Open the `.env_exapmle` file and edit as follows. After editing, rename the file to `.env`.

- AZURE_ENDPOINT_KEY=[*Primary Key*]
- AZURE_ENDPOINT_URL=https://[*Deploy Name*].[*Region*].inference.ml.azure.com/score
- AZURE_MODEL_DEPLOYMENT=[*Deploy Name*]

## Run Chainlit app
`chainlit run app.py`
