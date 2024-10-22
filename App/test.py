import customtkinter as ctk
from mongoCon import collection

# Create the main window
app = ctk.CTk()
app.title("CustomTkinter Search with Results")
app.geometry("800x800")

# Set theme and appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# Set the window background color to Tiffany Blue
tiffany_blue = "#65dff6"
app.configure(bg=tiffany_blue)

# Fetch a limited number of records from MongoDB
PAGE_SIZE = 5  # Define the number of records per page (changed to 5)
current_page = 0  # Start at page 0

def fetch_records(page):
    # Skip and limit results based on the page
    return list(collection.find({}, {"_id": 0, "title": 1, "tags": 1}).skip(page * PAGE_SIZE).limit(PAGE_SIZE))

# Create a search bar (CTkEntry) and center it horizontally
search_bar = ctk.CTkEntry(master=app, placeholder_text="Search here...", width=300, height=40, corner_radius=25, fg_color='white')
search_bar.pack(pady=10, padx=20, anchor='center')

# Add a search button below the search bar
search_button = ctk.CTkButton(master=app, text="Search", width=120, corner_radius=15)
search_button.pack(pady=10)

# Add a line separator
separator = ctk.CTkFrame(master=app, height=2, fg_color="black", bg_color=tiffany_blue)
separator.pack(fill='x', pady=10, padx=10)

# Create a scrollable frame to hold the title and tag cards
scrollable_frame = ctk.CTkScrollableFrame(master=app, width=700, height=500, bg_color=tiffany_blue, fg_color=tiffany_blue)
scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Function to display records with title and tags
def add_title_cards(records):
    # Clear existing widgets inside the scrollable frame
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Display each record's title and tags in cards
    for record in records:
        title = record.get("title", "No Title")
        tags = record.get("tags", [])  # Get tags as a list

        # Create a frame (card) for each title
        card_frame = ctk.CTkFrame(master=scrollable_frame, width=300, height=200, corner_radius=15, fg_color="white", bg_color=tiffany_blue)
        card_frame.pack(pady=10, padx=10)  # Padding for spacing between cards

        # Add title label to the card
        title_label = ctk.CTkLabel(master=card_frame, text=title, font=("Delius Swash Caps", 16), text_color="black")
        title_label.pack(pady=(10, 5), padx=10)

        # Add tags as rounded rectangles (like filters)
        tags_frame = ctk.CTkFrame(master=card_frame, fg_color="white", bg_color="white")  # Tag container frame
        tags_frame.pack(pady=5, padx=10, fill="x")

        for tag in tags:
            tag_label = ctk.CTkLabel(master=tags_frame, text=tag, font=("Delius Swash Caps", 12), text_color="black", fg_color="#ADD8E6", corner_radius=10, padx=5, pady=2)
            tag_label.pack(side="left", padx=5, pady=5)  # Adding margin between tags

# Pagination buttons
def next_page():
    global current_page
    current_page += 1
    records = fetch_records(current_page)
    if records:
        add_title_cards(records)
    else:
        current_page -= 1  # No more records, revert to previous page

def previous_page():
    global current_page
    if current_page > 0:
        current_page -= 1
        add_title_cards(fetch_records(current_page))

# Fetch the initial set of records and display
add_title_cards(fetch_records(current_page))

# Add pagination buttons
pagination_frame = ctk.CTkFrame(master=app, fg_color=tiffany_blue, height= 300)  # Frame for pagination buttons
pagination_frame.pack(pady=10, fill='x')  # Pack it to fill the width at the bottom

# Create buttons with increased height for better visibility
prev_button = ctk.CTkButton(master=pagination_frame, text="Previous", command=previous_page, width=100, height=40)
prev_button.pack(side="left", padx=10)

next_button = ctk.CTkButton(master=pagination_frame, text="Next", command=next_page, width=100, height= 40)
next_button.pack(side="left", padx=10)

# Start the main event loop
app.mainloop()
