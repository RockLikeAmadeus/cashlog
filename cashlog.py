
import numpy as np
import pandas as pd
from tabulate import tabulate

EXIT_CODES = ('X', 'x', 'exit', 'back')
ACTION_DIVIDER = "\n-----------------------------------\n\n"
SPACER = "\n\n\n\n\n\n"


def print_wallet(wallet):
    '''
    Prints envelope balances.
    Accepts a dataframe.
    '''
    print('\n' + tabulate(wallet[['envelope', 'balance']].values.tolist(), headers=['Envelope', 'Balance']))

def prompt_enter_txn():
    type, date, payee, payer = None, None, None, None
    envelope_from, envelope_to, notes = None, None, None
    prompt = ""
    # Transaction entry progress markers, so mistakes don't send us to the beginning of the loop
    type_entered, date_entered = False, False
    payee_entered, payer_entered = False, False
    envelope_from_entered, envelope_to_entered = False, False
    notes_entered = False
    while True:
        if (not type_entered):
            print("""
Enter Transaction Details:
Enter 'X' for any field when finished entering transactions.
Press return without entering a value into a field to use the value for that field specified in the previously entered transaction (excludes field 'Notes').
            """)
            # TYPE
            # TODO: Use a dictionary/map for the number-type relationship here
            prompt = "Type\n----------\n1 = Debit\n2 = Credit\n"
            if type != None:
                prompt += "Default = " + str(type)
            user_input = input(prompt + "Enter Transaction Type: ")
            if user_input in EXIT_CODES:
                break
            if user_input == "" and type == None:
                print(SPACER + "A value must be entered for field 'Type'.")
                continue
            elif user_input == "" and type != None:
                user_input = type
            type = user_input
            type_entered = True
        if (not date_entered):
            # DATE
            prompt = "\nDate\n----------\n"
            if date != None:
                prompt += "Default = " + str(date)
            user_input = input(prompt + "Enter Transaction Date: ")
            if user_input in EXIT_CODES:
                break
            if user_input == "" and date == None:
                print(SPACER + "A value must be entered for field 'Date'.")
                continue
            elif user_input == "" and date != None:
                user_input = date
            date = user_input
            date_entered = True

        # Reset for new transaction
        type_entered, date_entered = False, False
        payee_entered, payer_entered = False, False
        envelope_from_entered, envelope_to_entered = False, False
        notes_entered = False

def main():
    wallet = pd.read_csv("wallet.csv")
    print_wallet(wallet)

    action = ""
    while action not in EXIT_CODES:
        # TODO: Use an actual map/dictionary object to define which numbers correspond to which actions, and automate the generation of this string based on the dictionary
        print(ACTION_DIVIDER + "Available Tasks:\n1. Enter a transaction\n2. Allocate funds based on a pre-configured distribution\n3. Transfer funds between envelopes\nX. Exit\n")
        action = input("Choose a task: ")
        match action:
            case "1":
                print(SPACER)
                prompt_enter_txn()
            case _:
                if action in EXIT_CODES:
                    continue
                print(SPACER + "Please enter a number corresponding to the below listed available tasks. To exit, enter 'X'")

main()