from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import blog
from fastapi.responses import RedirectResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(blog.router)

@app.get("/")
def redirect_to_blogs():
    return RedirectResponse(url="/blogs")