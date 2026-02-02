import joblib

from fastapi import FastAPI
from contextlib import asynccontextmanager
from huggingface_hub import hf_hub_download
from pydantic import create_model

from app.utils import symptoms_list

ml_model = {}

REPO_ID = "AWeirdDev/human-disease-prediction"
FILENAME = "sklearn_model.joblib"

@asynccontextmanager
async def lifespan(app: FastAPI):
    ml_model["doctor"] = joblib.load(
        hf_hub_download(
            repo_id=REPO_ID, filename=FILENAME
        )
    )

    yield
    ml_model.clear()

app = FastAPI(title="AI Doctor", lifespan=lifespan)

query_parameters = {
    symp: (bool, False)
    for symp in symptoms_list[:10]
}

Symptoms = create_model(
    "Symptoms", **query_parameters
)

