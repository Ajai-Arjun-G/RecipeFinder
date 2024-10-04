import time
from CookWithManali import constants
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class recipes(webdriver.Chrome):
    
    disallowedPaths = [
    ]

    def __init__(self, executable_path="D:/chromedriver-win64/chromedriver.exe",options = Options(), teardown = False ):
        self.request_count = 0
        self.limit_time = 60  # seconds
        self.limit_requests = 15

        self.executable_path = executable_path
        self.options = options if options else webdriver.ChromeOptions()
        self.teardown = teardown
        self.options.add_argument("--no-sandbox") 
        self.options.binary_location = "D:/chrome-win64/chrome.exe"
        super(recipes, self).__init__(executable_path=self.executable_path, options=self.options)
        self.implicitly_wait(5)
        self.maximize_window()

    def landingPage(self):
        self.get(constants.CookWithManaliUrl)

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

    def wait_for_element(self, locator_type, locator):
        try:
            self.request_count += 1
            return WebDriverWait(self, 15).until(EC.presence_of_element_located((locator_type, locator)))
        except TimeoutException:
            print(f"Timeout while waiting for element: {locator}")
            return None

    def get_element_text(self, locator_type, locator):
        element = self.wait_for_element(locator_type, locator)
        self.request_count += 1
        return element.text if element else None
    
    def Browse(self):
        if self.request_count >= self.limit_requests:
            time.sleep(self.limit_time)
            self.request_count = 0  # Reset the counter after sleeping

        element = self.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/main/article/div/div[6]/div/div[2]')
        insideElement = element.find_elements(By.TAG_NAME, 'a')
        self.request_count += 1

        # Get the original window handle (main tab)
        original_window = self.current_window_handle

        for tag in insideElement:
            spanTag = tag.find_element(By.TAG_NAME, 'span')
            print(f"Span Text: {spanTag.text}")
            link = tag.get_attribute('href')
            self.request_count += 1
            self.execute_script(f"window.open('{link}', '_blank');")
            self.switch_to.window(self.window_handles[-1])

            pageNo = 0
            while pageNo < 5:
                # Wait for the list of recipes to appear
                ListofRecipes = self.wait_for_element(By.CLASS_NAME, "block-post-listing")
                if ListofRecipes is None:
                    break

                recipes = ListofRecipes.find_elements(By.CLASS_NAME, "post-summary")

                for each in recipes:
                    NewRecipe = each.find_element(By.CLASS_NAME, "post-summary__image")
                    self.request_count += 1
                    recipeLink = NewRecipe.find_element(By.TAG_NAME, "a")
                    self.request_count += 1

                    # Scroll the element into view
                    self.execute_script("arguments[0].scrollIntoView();", recipeLink)

                    # Wait for the element to be clickable
                    WebDriverWait(self, 15).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "post-summary__image"))
                    )

                    # Get the original window handle (main tab)
                    currentWindow = self.current_window_handle

                    link = recipeLink.get_attribute('href')
                    self.request_count += 1
                    self.execute_script(f"window.open('{link}', '_blank');")
                    self.switch_to.window(self.window_handles[-1])

                    # Extract recipe details
                    self.Title()
                    self.Ingredients()
                    self.Instructions()
                    self.CookTime()
                    self.Notes()
                    self.Nutrition()
                    self.Additional()

                    self.close()
                    self.switch_to.window(currentWindow)

                # Click the "Next" button if it exists
                try:
                    next_button = self.find_element(By.CLASS_NAME, "pagination-next")
                    self.request_count += 1
                    next_button.click()
                    pageNo += 1
                except TimeoutException:
                    print("No more pages available or ran into an error")
                    break

            # Close the current tab and switch back to the original window
            self.close()
            self.switch_to.window(original_window)


    def Title(self):
        title = self.get_element_text(By.CLASS_NAME, "wprm-recipe-name")
        if title:
            print(title)

    def CookTime(self):
        prepTime = self.get_element_text(By.CLASS_NAME, 'wprm-recipe-prep-time-container')
        cookTime = self.get_element_text(By.CLASS_NAME, 'wprm-recipe-cook-time-container')
        totalTime = self.get_element_text(By.CLASS_NAME, 'wprm-recipe-total-time-container')
        if prepTime and cookTime and totalTime:
            print(prepTime, type(prepTime), cookTime, totalTime)

    def Ingredients(self):
        ingredients = self.get_element_text(By.CLASS_NAME, 'wprm-recipe-ingredients')
        if ingredients:
            print(ingredients.split('\n'))

    def Instructions(self):
        instructions = self.get_element_text(By.CLASS_NAME, 'wprm-recipe-instructions')
        if instructions:
            print(instructions)

    def Notes(self):
        notes = self.get_element_text(By.CLASS_NAME, "wprm-recipe-notes")
        if notes:
            print(notes)

    def Nutrition(self):
        nutrients = self.get_element_text(By.CLASS_NAME, "cwp-food-nutrition")
        if nutrients:
            print(nutrients)

    def Additional(self):
        course = self.get_element_text(By.CLASS_NAME, "wprm-recipe-course-container")
        cuisine = self.get_element_text(By.CLASS_NAME, "wprm-recipe-cuisine-container")
        if course and cuisine:
            print(course, cuisine)