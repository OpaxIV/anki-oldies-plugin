# import the main window object (mw) from aqt
from aqt import mw, QAction

# import the "show info" tool from utils.py
from aqt.utils import showInfo
from aqt.qt import qconnect

# import all of the Qt GUI library
from aqt.qt import *

# input validation
import re

"""
Title: Anki Oldies Plugin
Description: The following file contains the logic for a small anki retirment plugin
Author: OpaxIV
Date: 22.04.2026
Version: 3.0
"""

##---------------------------------------------------------------------------------------------------------------------------------------------------------------- 

"""
NOTES / TODO:
    
"""


##---------------------------------------------------------------------------------------------------------------------------------------------------------------- 

"""
UserPrompt class for holding GUI window
utilise class for longer access to variables and functions
"""
class UserPrompt(QDialog):

    
    """
    Logic used to filter cards and move into new deck
    """
    def move_ivl(self) -> None:

        # Fetch data from Textbox and Dropdown Menu
        card_age = self.text_box.text()
        prop_ivl = f"prop:ivl{card_age}"                                                      # e.g., "prop:ivl>365"
        deck_name = self.ivl_deck_dropdown.currentText()

        # Parse input and handle errors
        if not validate(card_age):
            showInfo("Invalid prop_ivl")                                                      # invalid character found
            return  # stop execution here if error

        # return deck_id (no new deck is created)
        deck_id = mw.col.decks.id(deck_name)

        # Set filter for card search
        card_ids = mw.col.find_cards(prop_ivl)

        # Move cards to defined deck
        ret = mw.col.set_deck(card_ids=card_ids, deck_id=deck_id)

        # Get the count of successful operations
        success_operations = ret.count

        if success_operations:
            showInfo("Cards moved: %d" % success_operations)
        else:
            showInfo("Nothing to move")

    """
    Handle moving leeches into new deck
    """
    def move_leech(self):
        
        # Fetch data from Dropdown Menu
        deck_name = self.leech_deck_dropdown.currentText()

        # Get deck id
        deck_id = mw.col.decks.id(deck_name)

        # Filter cards by leech property
        card_ids = mw.col.find_cards("tag:leech")

        # Move cards to defined deck
        ret = mw.col.set_deck(card_ids=card_ids, deck_id=deck_id)

        # Get the count of successful operations
        success_operations = ret.count

        if success_operations:
            showInfo("Cards moved: %d" % success_operations)
        else:
            showInfo("Nothing to move")



    """
    Class initialisation
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # Define Groupbox and VBoxLayout objects
        self.group_box = QGroupBox("Retirement Settings")
        self.resize(400, 200)
        self.vbox = QVBoxLayout()                                                   # vertical box layout


        ## Ivl Card Handling
        # Text Box
        self.card_age_label= QLabel("Card Age")
        self.vbox.addWidget(self.card_age_label)
        self.ivl_subtitle_label = QLabel("Valid are positive numbers and combinations of arithmetic operators  \"<, >, =\"")
        self.ivl_subtitle_label.setStyleSheet("font-size: 10pt; color: gray;")
        self.vbox.addWidget(self.ivl_subtitle_label)

        self.text_box = QLineEdit()
        self.text_box.setText(">365")                                           # default value for text box
        self.vbox.addWidget(self.text_box)

        # Dropdown Menu
        self.ivl_dropdown_label = QLabel("Retirement Deck")
        self.vbox.addWidget(self.ivl_dropdown_label)
        self.ivl_dropdown_subtitle_label = QLabel("Choose a deck to move old cards into.")
        self.ivl_dropdown_subtitle_label.setStyleSheet("font-size: 10pt; color: gray;")
        self.vbox.addWidget(self.ivl_dropdown_subtitle_label)


        self.ivl_deck_dropdown = QComboBox()
        ivl_deck_list = mw.col.decks.all_names_and_ids()
        for deck in ivl_deck_list:
            self.ivl_deck_dropdown.addItem(deck.name, userData=deck.id)
        self.vbox.addWidget(self.ivl_deck_dropdown)

        # Buttons
        self.hbox = QHBoxLayout()                                      # horizontal box layout
        self.hbox.addStretch()                                                      # left spacer
        self.ivl_move_button= QPushButton("Move Old Cards")                  # move ivl button
        self.ivl_move_button.clicked.connect(self.move_ivl)
        self.hbox.addWidget(self.ivl_move_button)



        ## Leech Card Handling
        # Dropdown Menu
        self.leech_dropdown_label = QLabel("Leeches Deck")          #2do: add info about tagging of leeches
        self.vbox.addWidget(self.leech_dropdown_label)
        self.leech_dropdown_subtitle_label = QLabel("Choose a deck to move leeches into.")
        self.leech_dropdown_subtitle_label.setStyleSheet("font-size: 10pt; color: gray;")
        self.vbox.addWidget(self.leech_dropdown_subtitle_label)
        
        self.leech_deck_dropdown = QComboBox()
        leech_deck_list = mw.col.decks.all_names_and_ids()
        for deck in leech_deck_list:
            self.leech_deck_dropdown.addItem(deck.name, userData=deck.id)
        self.vbox.addWidget(self.leech_deck_dropdown)

        # Buttons
        #self.hbox = QHBoxLayout()                                                  # horizontal box layout --> use from before
        #self.hbox.addStretch()                                                     # left spacer
        self.leech_move_button= QPushButton("Move Leeches")            # move leeches button
        self.leech_move_button.clicked.connect(self.move_leech)
        self.hbox.addWidget(self.leech_move_button)



        ## Universal button to close user prompt
        self.close_button= QPushButton("Close")
        self.close_button.clicked.connect(self.reject)
        self.hbox.addWidget(self.close_button)
        self.hbox.addStretch()                                                      # right spacer


        ## Finalise Layout
        self.vbox.addLayout(self.hbox)                                      # add horizontal layout to vertical
        self.group_box.setLayout(self.vbox)


        # Set default coloring of Buttons and tabbing interaction
        self.ivl_move_button.setAutoDefault(False)
        self.leech_move_button.setAutoDefault(False)
        self.close_button.setDefault(True)
        self.close_button.setAutoDefault(False)

        # Create and set main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.group_box)
        self.setLayout(self.main_layout)




##---------------------------------------------------------------------------------------------------------------------------------------------------------------- 


"""
Validate ivl Input
"""
def validate(s):
    return re.match(r'^([<>]|=)\d+(\.\d+)?$', s.strip()) is not None



"""
Callback function when user runs "Anki Oldies Plugin" from the dropdown menu
"""
def show_prompt():
    if not hasattr(mw, "user_prompt") or not mw.user_prompt.isVisible():
        mw.user_prompt = UserPrompt(mw)
        mw.user_prompt.show()
    else:
        # Bring to front if already open
        mw.user_prompt.raise_()
        mw.user_prompt.activateWindow()

"""
Main function called when addon is initiated
"""
def main():

    # Create new entry in anki menu for the plugin
    action = QAction("Anki Oldies Plugin", mw)
    qconnect(action.triggered, show_prompt)       # only pass callback function, no direct call
    mw.form.menuTools.addAction(action)



##---------------------------------------------------------------------------------------------------------------------------------------------------------------- 

# anki addons are not called as modules
# execute main directly
main()
