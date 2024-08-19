from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from app.templates.data_models import MainDataModel


class PageController:
    def __init__(self) -> None:
        self.templates = Jinja2Templates(directory="app/templates")

    def main(self, request: Request, data: MainDataModel) -> _TemplateResponse:
        return self.templates.TemplateResponse(
            request=request,
            name="index.html",
            context=data.__dict__,
        )

    def global_dashboard(self, request: Request) -> _TemplateResponse:
        return self.templates.TemplateResponse(
            request=request,
            name="pages/global_dashboard.html",
            context={},
        )
