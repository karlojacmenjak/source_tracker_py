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
            context=data.model_dump(),
        )

    def global_dashboard(
        self,
        request: Request,
        data: DashboardDataModel,
    ) -> _TemplateResponse:

        return self.templates.TemplateResponse(
            request=request,
            name="pages/global_dashboard.html",
            context=data.model_dump(),
        )

    def guild_dashboard(self, request: Request, data: dict) -> _TemplateResponse:
        return self.templates.TemplateResponse(
            request=request,
            name="pages/guild_dashboard.html",
            context=data,
        )

    def page_404(self, request: Request) -> _TemplateResponse:
        return self.templates.TemplateResponse(
            request=request,
            name="pages/page_404.html",
            context={},
        )
