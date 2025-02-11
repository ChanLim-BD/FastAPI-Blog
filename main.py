from fastapi import FastAPI
from routes import blog
from fastapi.responses import RedirectResponse

app = FastAPI()
app.include_router(blog.router)

@app.get("/")
def redirect_to_blogs():
    return RedirectResponse(url="/blogs")