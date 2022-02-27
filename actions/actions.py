#from tensorflow import keras
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
from rasa_sdk.events import BotUttered
import sqlite3

# change this to the location of your SQLite file
path_to_db = "actions/example.db"

# class ActionProductOrder(Action):
#     def name(self) -> Text:
#         return "action_product_order"

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:

#         # connect to DB
#         connection = sqlite3.connect(path_to_db)
#         cursor = connection.cursor()

#         # # get slots and save as tuple
#         # shoe = [(tracker.get_slot("color")), (tracker.get_slot("size"))]

#           # get slots and save as tuple
#         shoe = [(tracker.get_slot("product_category")),(tracker.get_slot("color")), (tracker.get_slot("size")), (tracker.get_slot("gender")), (tracker.get_slot("style"))]
#         shoe_temp=shoe[1:3]
#         # place cursor on correct row based on search criteria
#         cursor.execute("SELECT * FROM inventory WHERE color=? AND size=?", shoe_temp)
#         # cursor.execute("SELECT * FROM inventory")
        
#         # retrieve sqlite row
#         data_row = cursor.fetchone()

#         if data_row:
#             # provide in stock message
#             dispatcher.utter_message(template="utter_in_stock")
#             dispatcher.utter_message(template="Do you want to place an order?")
            
#             connection.close()
#             slots_to_reset = ["product_category", "size", "color","gender","style"]
#             return [SlotSet(slot, None) for slot in slots_to_reset]
#         else:
#             # provide out of stock
#             dispatcher.utter_message(template="utter_no_stock")
#             connection.close()
#             slots_to_reset = ["product_category", "size", "color","gender","style"]
#             return [SlotSet(slot, None) for slot in slots_to_reset]

class ActionProductSearch(Action):
    def name(self) -> Text:
        return "action_product_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # # get slots and save as tuple
        # shoe = [(tracker.get_slot("color")), (tracker.get_slot("size"))]

         # get slots and save as tuple
        shoe = [(tracker.get_slot("product_category")),(tracker.get_slot("color")), (tracker.get_slot("size")), (tracker.get_slot("gender")), (tracker.get_slot("style"))]
        shoe_temp=shoe[1:3]
        # place cursor on correct row based on search criteria
        cursor.execute("SELECT * FROM inventory WHERE color=? AND size=? AND product_category=? AND gender=? AND style=? ", shoe)
        # cursor.execute("SELECT * FROM inventory")
        
        # retrieve sqlite row
        #data_row = cursor.fetchone()
        data_row = cursor.fetchall()

        if data_row:
            # provide in stock message
            
            for row in data_row:
                size = row[0][0]
                color = row[0][1]
                gender = row[0][2]
                product_category = row[0][3]
                style = row[0][4]
                # dispatcher.utter_message(template="utter_in_stock")
                dispatcher.utter_message(size, color, gender, product_category, style)
                
            connection.close()
            slots_to_reset = ["product_category", "size", "color","gender","style"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
        else:
            # provide out of stock
            dispatcher.utter_message(template="utter_no_stock")
            connection.close()
            slots_to_reset = ["product_category", "size", "color","gender","style"]
            return [SlotSet(slot, None) for slot in slots_to_reset]

class SurveySubmit(Action):
    def name(self) -> Text:
        return "action_survey_submit"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_open_feedback")
        dispatcher.utter_message(template="utter_survey_end")
        return [SlotSet("survey_complete", True)]


class OrderStatus(Action):
    def name(self) -> Text:
        return "action_order_status"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get email slot
        order_email = (tracker.get_slot("email"),)

        # retrieve row based on email
        cursor.execute("SELECT * FROM orders WHERE order_email=?", order_email)
        data_row = cursor.fetchone()

        if data_row:
            # convert tuple to list
            data_list = list(data_row)

            # respond with order status
            dispatcher.utter_message(template="utter_order_status", status=data_list[5])
            connection.close()
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(template="utter_no_order")
            connection.close()
            return []


class CancelOrder(Action):
    def name(self) -> Text:
        return "action_cancel_order"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get email slot
        order_email = (tracker.get_slot("email"),)

        # retrieve row based on email
        cursor.execute("SELECT * FROM orders WHERE order_email=?", order_email)
        data_row = cursor.fetchone()

        if data_row:
            # change status of entry
            status = [("cancelled"), (tracker.get_slot("email"))]
            cursor.execute("UPDATE orders SET status=? WHERE order_email=?", status)
            connection.commit()
            connection.close()

            # confirm cancellation
            dispatcher.utter_message(template="utter_order_cancel_finish")
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(template="utter_no_order")
            connection.close()
            return []


class ReturnOrder(Action):
    def name(self) -> Text:
        return "action_return"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get email slot
        order_email = (tracker.get_slot("email"),)

        # retrieve row based on email
        cursor.execute("SELECT * FROM orders WHERE order_email=?", order_email)
        data_row = cursor.fetchone()

        if data_row:
            # change status of entry
            status = [("returning"), (tracker.get_slot("email"))]
            cursor.execute("UPDATE orders SET status=? WHERE order_email=?", status)
            connection.commit()
            connection.close()

            # confirm return
            dispatcher.utter_message(template="utter_return_finish")
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(template="utter_no_order")
            connection.close()
            return []

class GiveName(Action):
    def name(self) -> Text:
        return "action_give_name"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        evt = BotUttered(
            text = "my name is bot? idk", 
            metadata = {
                "nameGiven": "bot"
            }
        )

        return [evt]