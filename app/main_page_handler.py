from handler import Handler


class MainPage(Handler):
    def get(self):
        self.render('blog/home.html')

    def post(self):
        pass