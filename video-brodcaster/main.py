# conda activate broadcaster_live 
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")


@app.get("/devices")
def list_devices():
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
