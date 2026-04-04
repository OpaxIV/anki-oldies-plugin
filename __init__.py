# import the main window object (mw) from aqt
from aqt import mw


# import the "show info" tool from utils.py
from aqt.utils import showInfo
from aqt.qt import qconnect

# import all of the Qt GUI library
from aqt.qt import *







# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction() -> None:
    # get the number of cards in the current collection, which is stored in
    
    # the main window
    ##cardCount = mw.col.card_count()

    card_ids = mw.col.find_cards("prop:ivl<1")
    ##cards = [mw.col.get_card(cid) for cid in card_ids]

    """
    if cards:
        showInfo("First Card question: %s" % cards[0].question())
    else:
        showInfo("No cards found")

    """


    ## create a deck if not exist
    deck_id = mw.col.decks.id("Retirement")

    ## move cards to deck
    ret = mw.col.set_deck(card_ids=card_ids, deck_id=deck_id)

    ## get the count of successfull operations
    success_operations = ret.count

    if success_operations:
        showInfo("Card count: %d" % success_operations)
    else:
        showInfo("Nothing to move")



# create a new menu item, "test"
action = QAction("Run Retirement", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
