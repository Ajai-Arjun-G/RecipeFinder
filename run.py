from BBC_Good_Food.recipes import recipes

#Creating a sample instance
# inst = NDTV_News()
# inst.landingPage()

with recipes() as bot:
    bot.landingPage()
    bot.CookiesPopUp()
    bot.Ingredients()