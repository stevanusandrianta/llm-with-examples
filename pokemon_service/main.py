from typing import Union
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

elements_db = {
    "bulbasaur": ["grass", "poison"],
    "charmander": ["fire"],
    "squirtle": ["water"],
}

@app.get("/")
def read_root():
    return {"Hello": "Pokemon"}

@app.get("/pokemon/{pokemon_name}")
def get_elements(pokemon_name: str):
    pokemon_name = pokemon_name.lower()
    if len(elements_db.get(pokemon_name, [])) == 0:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    else:
        return {
            "pokemon_name": pokemon_name, 
            "elements": elements_db.get(pokemon_name)
        }
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)