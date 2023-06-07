from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib

# Load the trained model
model = joblib.load('model/lr_model.pkl')
vectorizer = joblib.load('model/lr_cvectorizer.joblib')

class AddressRequest(BaseModel):
    address: str

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_model(address: str) -> bool:
    # Vectorize the input string
    vectorized_input = vectorizer.transform([address])
    # Make predictions using the loaded model
    predictions = model.predict(vectorized_input)
    result = predictions[0]
    print(f'For address: {address}. Result: {result}')
    return result

@app.post('/is_address')
async def verify_address(request: AddressRequest):
    #import pdb; pdb.set_trace()
    try:
        address = request.address
        is_valid = run_model(str(address))

        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail='Invalid Address'
            )

        response = {
            'status_code': 'SUCCESS',
            'status': 200,
            'data'  :'Valid Address'
        }

        return response
    
    except HTTPException as err:
        return {
            'status_code': 'ERROR',
            'status': err.status_code,
            'data': err.detail
        }
