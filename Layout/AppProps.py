class AppProps():
    def __init__(self, app):
        print("LayoutProps - init")

        self.app = app
        # Defaults
        self.title = '0x432d2d'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480

        self.min_width = .3 # Proportion of screen width
        self.resizable = True
