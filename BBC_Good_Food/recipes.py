from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class NDTV_News(webdriver.Chrome):
    disallowedPaths = [
        "/images/ndtvvideo/*",
        "/news/redirect/*",
        "/news/feeds/*",
        "/page/send-email/",
        "/mb/",
        "/usopen09/",
        "/ndtvfuture/",
        "/video/embed-player",
        "/ndtvfuture/ndtv/postcomments.aspx"
    ]

    def __init__(self, executable_path="D:/chromedriver-win64/chromedriver.exe",options = Options(), teardown = False ):
        self.executable_path = executable_path
        self.options = options if options else webdriver.ChromeOptions()
        self.teardown = teardown
        self.options.add_argument("--no-sandbox") 
        self.options.binary_location = "D:/chrome-win64/chrome.exe"
        super(NDTV_News, self).__init__(executable_path=self.executable_path, options=self.options)
        self.implicitly_wait(5)
        self.maximize_window()
