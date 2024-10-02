from BBC_Good_Food.constants import *

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

class recipes(webdriver.Chrome):
    disallowedPaths = [
        "User-agent: *",
        "Disallow: /wp-admin/",
        "Disallow: /4817/",
        "Disallow: /176986657/",
        "Disallow: /styleguide/",
        "Disallow: /author/mrben/",
        "Disallow: /members/",
        "Disallow: /account/",
        "Disallow: /signin/",
        "Disallow: /account/",
        "Disallow: /auth/",
        "Disallow: /search/recipes/?q=",
        "Disallow: /search/recipes/?sort=",
        "Disallow: /search/recipes/page/",
        "Disallow: /search/node",
        "Disallow: /api/",
        "Disallow: /article/welcome-email",
        "Disallow: /article/thank-you-registering",
        "Disallow: /article/thank-you-signing-health-edit",
        "Disallow: *null?",
        "Disallow: *obOrigUrl=true",
        "Disallow: /seasonal-calendar/all",
        "Disallow: /Search?searchstring_input=",
        "Disallow: /v1/",
        "Disallow: *wp-sitemap-taxonomies-post_tag",
        "Disallow: /user/login",
        "Disallow: /search",
        "Disallow: /search-results/",
        "Disallow: /user/*/collections/",
        "Disallow: /user/*/collection/",
        "Disallow: /user/register",
        "Disallow: /wp-sitemap-posts-",

        "Disallow: /list-v2/",
        "Disallow: /article-v2/",
        "Disallow: /search-results/",

        "Disallow: /registration",
        "Disallow: /registration/",
        "Disallow: /forgotten-password",
        "Disallow: /forgotten-password/",
        "Disallow: /change-password/",
        "Disallow: /reset-password",
        "Disallow: /reset-password/",
        "Disallow: /login",
        "Disallow: /login/",
        "Disallow: /log-out",
        "Disallow: /log-out/"
    ]

    def __init__(self, executable_path="D:/chromedriver-win64/chromedriver.exe",options = Options(), teardown = False ):
        self.executable_path = executable_path
        self.options = options if options else webdriver.ChromeOptions()
        self.teardown = teardown
        self.options.add_argument("--no-sandbox") 
        self.options.binary_location = "D:/chrome-win64/chrome.exe"
        super(recipes, self).__init__(executable_path=self.executable_path, options=self.options)
        self.implicitly_wait(5)
        self.maximize_window()

    def landingPage(self):
        self.get(BBCGoodFoodUrl)

    def __exit__(self, *args):
        if self.teardown:
            self.quit()

    def CookiesPopUp(self):
        action =  ActionChains(self)
        element = self.find_element_by_xpath("/html/body/div/div[2]")
        if element:
            frame = self.find_element_by_id('sp_message_iframe_1175834')
            self.switch_to.frame(frame)
            button = self.find_element_by_xpath("/html/body/div/div[2]/div[3]/button[2]")
            action.click(on_element = button)
            action.perform()

        
    def Ingredients(self):
        self.switch_to.default_content()
        element = self.find_element_by_xpath('/html/body/div[1]/div[4]/main/div[2]/div/div[3]/div[1]/div[1]/div[5]/div/div[1]/section/section/ul')
        ingredients = element.text
        print(ingredients.split('\n'))

    def Instructions(self):
        element = self.find_element_by_class_name('grouped-list__list')
        instructions = element.text
        print(instructions)

