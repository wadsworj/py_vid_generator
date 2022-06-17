from src.uilayer.elementsview.elementsview import ElementsView
from src.uilayer.elementsview.elementsviewpresenter import ElementsViewPresenter
from src.video import Video


class ElementsViewBuilder:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager

    def build(self, data, parent: Video):
        presenter = ElementsViewPresenter()

        view = ElementsView(parent, data, parent.screen, self.ui_manager)
        view.ui_manager = self.ui_manager
        view.presenter = presenter

        presenter.view = view
        presenter.data = data

        return view
