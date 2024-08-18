from app.controllers import PageController


class ControllerFactory:

    def get_page_controller(self) -> PageController:
        return PageController()
