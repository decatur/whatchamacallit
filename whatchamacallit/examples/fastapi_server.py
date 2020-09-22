import uvicorn
from starlette.responses import RedirectResponse
from fastapi import FastAPI
from whatchamacallit.fastapi import register

app = FastAPI()
register(app)


@app.get("/")
async def get_home():
    return RedirectResponse(url='/index.html')


# app.mount("/", StaticFiles(directory="."), name="static")

uvicorn.run(app, host="0.0.0.0", port=8081, access_log=True, log_level="trace", workers=1, debug=False)
