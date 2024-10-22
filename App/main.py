import customtkinter as ctk
from mongoCon import collection

# Create the main window
app = ctk.CTk()
app.title("Recipe Finder")
app.geometry("800x800")

# Set theme and appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


tiffany_blue = "#65dff6"
suggestion_color = "#f0f8ff"  

app.configure(bg=tiffany_blue)

PAGE_SIZE = 5
current_page = 0

def fetch_records(page, query=None):
    if query:
        return list(collection.find(
            {"$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"tags": {"$regex": query, "$options": "i"}}
            ]},
            {"_id": 0, "title": 1, "tags": 1}
        ).skip(page * PAGE_SIZE).limit(PAGE_SIZE))
    else:
        return list(collection.find({}, {"_id": 0, "title": 1, "tags": 1}).skip(page * PAGE_SIZE).limit(PAGE_SIZE))

def fetch_recipe_details(title):
    return collection.find_one({"title": title})

# search bar
search_bar_frame = ctk.CTkFrame(master=app, fg_color=tiffany_blue)
search_bar_frame.pack(fill="x", pady=10)

search_bar = ctk.CTkEntry(master=search_bar_frame, placeholder_text="Search here...", width=300, height=40, corner_radius=25, fg_color='#cbebf5')
search_bar.pack(pady=10, padx=20, anchor='center')


suggestion_list = ctk.CTkScrollableFrame(master=search_bar_frame, width=300, height=150, fg_color=suggestion_color)
suggestion_list.pack(pady=(0, 10), padx=20, anchor='center')
suggestion_list.pack_forget()  

def fetch_suggestions(query):
    suggestions = list(collection.find(
        {"title": {"$regex": query, "$options": "i"}},
        {"_id": 0, "title": 1}
    ).limit(5)) 
    return [suggestion["title"] for suggestion in suggestions]

def show_suggestions(suggestions):
    
    for widget in suggestion_list.winfo_children():
        widget.destroy()

    if suggestions:
        suggestion_list.pack(pady=(0, 10), padx=20, anchor='center')  

        for title in suggestions:
            suggestion_label = ctk.CTkLabel(master=suggestion_list, text=title, font=("Delius Swash Caps", 12), text_color="black")
            suggestion_label.pack(pady=5)

            
            suggestion_label.bind("<Button-1>", lambda event, title=title: select_suggestion(title))

    else:
        suggestion_list.pack_forget()  

def select_suggestion(title):
    search_bar.delete(0, ctk.END)  
    search_bar.insert(0, title)      
    perform_search()                  

def on_search_change(event):
    query = search_bar.get()
    if query:
        suggestions = fetch_suggestions(query)
        show_suggestions(suggestions)
    else:
        suggestion_list.pack_forget() 

search_bar.bind("<KeyRelease>", on_search_change)


def perform_search():
    global current_page
    query = search_bar.get()
    current_page = 0
    records = fetch_records(current_page, query)
    add_title_cards(records)

search_button = ctk.CTkButton(master=search_bar_frame, text="Search", command=perform_search, width=100, height=40, corner_radius=20, fg_color="#cbebf5", text_color="black")
search_button.pack(pady=10)


separator_frame = ctk.CTkFrame(master=app, height=2, fg_color=tiffany_blue)
separator_frame.pack(fill='x', pady=0, padx=10)

separator = ctk.CTkFrame(master=separator_frame, height=2, fg_color="black")
separator.pack(fill='x')

scrollable_frame = ctk.CTkScrollableFrame(master=app, width=700, height=500, bg_color=tiffany_blue, fg_color=tiffany_blue)
scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

def add_title_cards(records):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    for record in records:
        title = record.get("title", "No Title")
        tags = record.get("tags", [])

        card_frame = ctk.CTkFrame(master=scrollable_frame, width=300, height=150, corner_radius=15, fg_color="#cbebf5")
        card_frame.pack(pady=10, padx=10)

        title_label = ctk.CTkLabel(master=card_frame, text=title, font=("Delius Swash Caps", 16), text_color="black")
        title_label.pack(pady=(10, 5), padx=10)

        tags_frame = ctk.CTkFrame(master=card_frame, fg_color="#cbebf5")
        tags_frame.pack(pady=5, padx=10, fill="x")

        for tag in tags:
            tag_label = ctk.CTkLabel(master=tags_frame, text=tag, font=("Delius Swash Caps", 12), text_color="black", fg_color="lightblue", corner_radius=10, padx=5, pady=2)
            tag_label.pack(side="left", padx=5, pady=5, anchor="w")

      
        card_frame.bind("<Button-1>", lambda event, title=title: open_recipe_window(title))

def open_recipe_window(title):
    recipe_details = fetch_recipe_details(title)
    if recipe_details:
  
        recipe_window = ctk.CTkToplevel(app)
        recipe_window.title(title)
        recipe_window.geometry("600x600")
        
    
        title_label = ctk.CTkLabel(master=recipe_window, text=recipe_details["title"], font=("Delius Swash Caps", 20), text_color="black")
        title_label.pack(pady=10)

        # Tags
        tags_label = ctk.CTkLabel(master=recipe_window, text="Tags: " + ", ".join(recipe_details.get("tags", [])), font=("Delius Swash Caps", 12), text_color="black")
        tags_label.pack(pady=5)

        # Ingredients
        ingredients_label = ctk.CTkLabel(master=recipe_window, text="Ingredients:", font=("Delius Swash Caps", 16), text_color="black")
        ingredients_label.pack(pady=10)

        ingredients_text = ctk.CTkTextbox(master=recipe_window, width=500, height=100)
        ingredients_text.pack(pady=5)
        ingredients_text.insert("0.0", "\n".join(recipe_details.get("ingredients", [])))
        ingredients_text.configure(state="disabled")  # Make it read-only

        # Instructions
        instructions_label = ctk.CTkLabel(master=recipe_window, text="Instructions:", font=("Delius Swash Caps", 16), text_color="black")
        instructions_label.pack(pady=10)

        instructions_text = ctk.CTkTextbox(master=recipe_window, width=500, height=150)
        instructions_text.pack(pady=5)
        instructions_text.insert("0.0", "\n".join(recipe_details.get("instructions", "")))
        instructions_text.configure(state="disabled")  # Make it read-only

        # Nutritional Information
        nutrients_label = ctk.CTkLabel(master=recipe_window, text="Nutritional Information:", font=("Delius Swash Caps", 16), text_color="black")
        nutrients_label.pack(pady=10)

        nutrients_text = ctk.CTkTextbox(master=recipe_window, width=500, height=100)
        nutrients_text.pack(pady=5)
        nutrients = recipe_details.get("nutrition")
        for i in nutrients:
            print(i)
        nutrients_text.insert("0.0",  "\n".join(recipe_details.get("nutrition", "N/A")))
        nutrients_text.configure(state="disabled") 

initial_records = fetch_records(current_page)
if initial_records:
    add_title_cards(initial_records)

def next_page():
    global current_page
    current_page += 1
    records = fetch_records(current_page, search_bar.get())
    add_title_cards(records)

def previous_page():
    global current_page
    if current_page > 0:
        current_page -= 1
        records = fetch_records(current_page, search_bar.get())
        add_title_cards(records)


pagination_frame = ctk.CTkFrame(master=app, fg_color=tiffany_blue, width=700)
pagination_frame.pack(pady=10, side="bottom")

prev_button = ctk.CTkButton(master=pagination_frame, text="Previous", command=previous_page, width=100, fg_color="#cbebf5", text_color="black")
prev_button.pack(side="left", padx=20)

next_button = ctk.CTkButton(master=pagination_frame, text="Next", command=next_page, width=100, fg_color="#cbebf5", text_color="black")
next_button.pack(side="right", padx=20)

app.mainloop()
