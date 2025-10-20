from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def read_root():
    return {'Hello': 'Synerchat'}

@app.get('/healthz')
def healthz():
    return {'ok': True}
