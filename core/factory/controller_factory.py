from app.controllers import PageController


class ControllerFactory:

    @staticmethod
    def get_page_controller() -> PageController:
        return PageController()
