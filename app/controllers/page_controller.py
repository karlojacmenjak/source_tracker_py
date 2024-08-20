from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from app.models.template import DashboardDataModel, MainDataModel


class PageController:
    def __init__(self) -> None:
        self.templates = Jinja2Templates(directory="app/templates")

    def main(self, request: Request, data: MainDataModel) -> _TemplateResponse:
        return self.templates.TemplateResponse(
            request=request,
            name="index.html",
            context=data.__dict__,
        )

    def global_dashboard(
        self, request: Request, data: DashboardDataModel
    ) -> _TemplateResponse:

        print(data.__dict__)
        return self.templates.TemplateResponse(
            request=request,
            name="pages/global_dashboard.html",
            context={},
        )
