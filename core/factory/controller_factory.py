from app.controllers import IPCController, PageController


class ControllerFactory:

    def get_page_controller(self) -> PageController:
        return PageController()

    def get_ipc_controller(self) -> IPCController:
        return IPCController()
