from core.controllers.page_controller import PageController


class ControllerFactory:

    def get_page_controller(self) -> PageController:
        return PageController()
