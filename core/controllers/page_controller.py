from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse


class PageController:
    def __init__(self) -> None:
        self.templates = Jinja2Templates(directory="app/templates")

    def main(self, request: Request) -> _TemplateResponse:
        return self.templates.TemplateResponse(
            request=request,
            name="main.j2",
            context={},
        )
