import time
import rdflib
from CookWithManali import constants
from CookWithManali import db,collection,nlp,g
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="rdflib.term")


class recipes(webdriver.Chrome):
    
    disallowedPaths = [
    ]

    def __init__(self, executable_path="D:/chromedriver-win64/chromedriver.exe",options = Options(), teardown = False ):
        self.request_count = 0
        self.limit_time = 2  # seconds
        self.limit_requests = 20

        self.executable_path = executable_path
        self.options = options if options else webdriver.ChromeOptions()
        self.teardown = teardown
        self.options.add_argument("--no-sandbox") 
        self.options.binary_location = "D:/chrome-win64/chrome.exe"
        super(recipes, self).__init__(executable_path=self.executable_path, options=self.options)
        self.implicitly_wait(3)
        self.maximize_window()
        self.all_recipes = []  # To store all recipe data

    def store_recipe(self, title, ingredients, instructions, cook_time, notes, nutrition, additional, tags):

        ingredients = [ingredient for ingredient in ingredients if ingredient.strip() != '▢']

        recipe_data = {
            "title": title,
            "ingredients": ingredients,
            "instructions": instructions,
            "cook_time": cook_time,
            "notes": notes,
            "nutrition": nutrition,
            "additional": additional,
            "tags":tags
        }
        result = collection.insert_one(recipe_data)
        self.all_recipes.append(recipe_data)

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
            return WebDriverWait(self, 3).until(EC.presence_of_element_located((locator_type, locator)))
        except TimeoutException:
            print(f"Timeout while waiting for element: {locator}")
            return None

    def get_element_text(self, locator_type, locator):
        element = self.wait_for_element(locator_type, locator)
        self.request_count += 1
        return element.text if element else None


    def queryOntology(self, ingredients):
        # Suppress specific rdflib warnings
        warnings.filterwarnings("ignore", category=UserWarning, module="rdflib.term")
        tags = []

        for element in ingredients:
            doc = nlp(element)

            # Collect pairs of nouns and standalone nouns
            i = 0
            extracted_nouns = []

            while i < len(doc):
                if doc[i].pos_ == 'NOUN':
                    # Check if the next token is also a noun for multi-word pairing
                    if i + 1 < len(doc) and doc[i + 1].pos_ == 'NOUN':
                        # Form a pair and add it to the extracted nouns
                        noun_pair = f"{doc[i].lemma_.lower()} {doc[i + 1].lemma_.lower()}"
                        extracted_nouns.append(noun_pair)
                        i += 2  # Skip the next noun since it's already paired
                    else:
                        # Add the standalone noun
                        extracted_nouns.append(doc[i].lemma_.lower())
                        i += 1
                else:
                    i += 1  # Move to the next token

            # Remove duplicates by converting to a set, then back to a list
            extracted_nouns = set(extracted_nouns)
            print(extracted_nouns)

            # Query the ontology for the identified nouns
            for each in extracted_nouns:
                query = f"""
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX obo: <http://purl.obolibrary.org/obo/>

                    SELECT ?term ?label
                    WHERE {{
                        ?term rdfs:label ?label .
                        FILTER (regex(?label, "{each}", "i"))
                    }}
                """
                results = g.query(query)

                # If no matches found for the multi-word noun, check for individual words
                if len(results) == 0:
                    # Split the noun into individual words
                    individual_nouns = each.split()
                    for individual in individual_nouns:
                        individual_query = f"""
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX obo: <http://purl.obolibrary.org/obo/>

                            SELECT ?term ?label
                            WHERE {{
                                ?term rdfs:label ?label .
                                FILTER (regex(?label, "{individual}", "i"))
                            }}
                        """
                        individual_results = g.query(individual_query)
                        if len(individual_results) > 0:
                            tags.append(individual)

                # If matches were found for the multi-word noun, add it to the tags
                if len(results) > 0:
                    tags.append(each)

        return list(set(tags))

    
    def Browse(self):
        if self.request_count >= self.limit_requests:
            time.sleep(self.limit_time)
            self.request_count = 0  # Reset the counter after sleeping

        element = self.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/main/article/div/div[6]/div/div[2]')
        insideElement = element.find_elements(By.TAG_NAME, 'a')

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
            while pageNo < 4:
                # Wait for the list of recipes to appear
                ListofRecipes = self.wait_for_element(By.CLASS_NAME, "block-post-listing")
                if ListofRecipes is None:
                    break

                recipes = ListofRecipes.find_elements(By.CLASS_NAME, "post-summary")

                for each in recipes:
                    NewRecipe = each.find_element(By.CLASS_NAME, "post-summary__image")
                    recipeLink = NewRecipe.find_element(By.TAG_NAME, "a")

                    # Scroll the element into view
                    self.execute_script("arguments[0].scrollIntoView();", recipeLink)

                    # Wait for the element to be clickable
                    WebDriverWait(self, 15).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "post-summary__image"))
                    )

                    # Get the original window handle (main tab)
                    currentWindow = self.current_window_handle

                    link = recipeLink.get_attribute('href')
                    self.execute_script(f"window.open('{link}', '_blank');")
                    self.switch_to.window(self.window_handles[-1])

                    # Extract recipe details
                    self.extract_recipe()

                    if self.request_count >= self.limit_requests:
                        print("going to sleep")
                        time.sleep(self.limit_time)
                        self.request_count = 0 

                    self.close()
                    self.switch_to.window(currentWindow)

                # Click the "Next" button if it exists
                try:
                    next_button = self.wait_for_element(By.CLASS_NAME,"pagination-next")
                    if next_button:
                        next_button = self.find_element_by_class_name("pagination-next")
                        self.execute_script("arguments[0].scrollIntoView(true);", next_button)
                        pageNo += 1
                        next_button.click()
                        print(pageNo)
                    else:
                        break
                except TimeoutException:
                    print("No more pages available or ran into an error")
                    self.close()


            # Close the current tab and switch back to the original window
            self.close()
            self.switch_to.window(original_window)


    def Title(self):
        title = self.get_element_text(By.CLASS_NAME, "wprm-recipe-name")
        if title:
            return title

    def CookTime(self):
        prepTime = self.get_element_text(By.CLASS_NAME, 'wprm-recipe-prep-time-container')
        cookTime = self.get_element_text(By.CLASS_NAME, 'wprm-recipe-cook-time-container')
        totalTime = self.get_element_text(By.CLASS_NAME, 'wprm-recipe-total-time-container')
        if prepTime or cookTime or totalTime:
            return {"prep_time": prepTime, "cook_time": cookTime, "total_time": totalTime}

    def Ingredients(self):
        Setingredients = set()
        ingredients = self.get_element_text(By.CLASS_NAME, 'wprm-recipe-ingredients')
        ingredients = ingredients.split('\n')
        if ingredients:
            ingredients = [ingredient for ingredient in ingredients if ingredient.strip() != '▢']
            return ingredients

    def Instructions(self):
        instructions = self.get_element_text(By.CLASS_NAME, 'wprm-recipe-instructions')
        if instructions:
            return instructions.split("\n")

    def Notes(self):
        notes = self.get_element_text(By.CLASS_NAME, "wprm-recipe-notes")
        if notes:
            return notes

    def Nutrition(self):
        nutrients = self.get_element_text(By.CLASS_NAME, "cwp-food-nutrition")
        if type(nutrients) == str and nutrients == "Nutrition information is automatically calculated, so should only be used as an approximation." :
            return 
        else:
            nutrients = nutrients.split(',')
            return nutrients

    def Additional(self):
        course = self.get_element_text(By.CLASS_NAME, "wprm-recipe-course-container")
        cuisine = self.get_element_text(By.CLASS_NAME, "wprm-recipe-cuisine-container")
        if course or cuisine:
            return {"course": course, "cuisine": cuisine}
        
    def extract_recipe(self):
        try:
            title = self.Title()
            ingredients = self.Ingredients()
            instructions = self.Instructions()
            cook_time = self.CookTime()
            notes = self.Notes()
            nutrition = self.Nutrition()
            additional = self.Additional()
            tags = self.queryOntology(ingredients)
            print("no problem")
            print(tags)

            # Store the recipe in the list
            self.store_recipe(title, ingredients, instructions, cook_time, notes, nutrition, additional,tags)
        except Exception as e:
            print(f"Error extracting recipe: {e}")