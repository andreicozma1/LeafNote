class LayoutProps():
    def __init__(self, app):
        print("LayoutProps - init")

        self.app = app
        self.min_doc_width = .4
        self.min_menu_width = .2
        self.max_menu_width = .3
        self.bar_height = 30

        self.splitter_width = 1
