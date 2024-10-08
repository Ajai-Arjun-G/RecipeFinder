import BBC_Good_Food
import BBC_Good_Food.recipes
import CookWithManali
import CookWithManali.recipes
import CookWithManali.constants

#Creating a sample instance
# inst = NDTV_News()
# inst.landingPage()

def ExtractBBCGoodFood():

    # With block will automatically call on a exit method once done executing, 
    # So we have to define one for sure if we want to use with in our code.
    with BBC_Good_Food.recipes.recipes() as bot:
        bot.landingPage()
        bot.CookiesPopUp()
        bot.Ingredients()
        bot.Instructions()

def ExtractCookWithManali():
    with CookWithManali.recipes.recipes() as bot:
        bot.landingPage()
        bot.Browse()

ExtractCookWithManali()
print(CookWithManali.recipes.recipes().all_recipes)