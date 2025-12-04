from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(request: Request, error: str | None = None):
    return templates.TemplateResponse(
        "index.html", {"request": request, "error": error}
    )
