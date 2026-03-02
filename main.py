from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routers import (
    home_router,
    invoice_router
)

# define ASGI
app = FastAPI(title="Intelligent Document Processing")
# define templates
templates = Jinja2Templates(directory="templates")

# include Routers
app.include_router(home_router.router)
app.include_router(invoice_router.router)


# Global excepiton Handler
@app.exception_handler(HTTPException)
async def global_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "error": exc.detail

        },
        status_code=exc.status_code
    )