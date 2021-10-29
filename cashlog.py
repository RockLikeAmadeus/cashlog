
import numpy as np
import pandas as pd
from tabulate import tabulate

EXIT_CODES = ('X', 'x', 'exit', 'back')
ACTION_DIVIDER = "\n-----------------------------------\n\n"
SPACER = "\n\n\n\n\n\n"
HORIZONTAL_RULE_SHORT = "\n----------\n"

# Enumerations
TASKS = { 
    1: "Enter a transaction",
    2: "Allocate funds based on a pre-configured distribution",
    3: "Transfer funds between envelope",
    "X": "Exit" 
}
TRANSACTION_TYPE = { 1: "Debit", 2: "Credit" }


def print_wallet(wallet):
    '''
    Prints envelope balances.
    Accepts a dataframe.
    '''
    print('\n' + tabulate(wallet[['envelope', 'balance']].values.tolist(), headers=['Envelope', 'Balance']))

def prompt_enter_txn():
    type, prev_type = None, None
    date, prev_date = None, None
    payee, prev_payee = None, None
    payer, prev_payer = None, None
    envelope_from, prev_envelope_from = None, None
    envelope_to, prev_envelope_to = None, None
    notes, prev_notes = None, None
    prompt = ""
    while True:
        if type == None:
            print("""
Enter Transaction Details:
Enter 'X' for any field when finished entering transactions.
Press return without entering a value into a field to use the value for that field specified in the previously entered transaction (excludes field 'Notes').
            """)
            # TYPE
            prompt = "Type" + HORIZONTAL_RULE_SHORT 
            for key in TRANSACTION_TYPE:
                prompt += str(key) + " = " + TRANSACTION_TYPE[key] + "\n"
            if prev_type != None:
                prompt += "Default = " + str(prev_type) + "\n\n"
            else:
                prompt += "\n"
            user_input = input(prompt + "Enter Transaction Type: ")
            if user_input in EXIT_CODES:
                break
            if user_input == "" and prev_type == None:
                print(SPACER + "A value must be entered for field 'Type'.")
                continue
            elif user_input == "" and prev_type != None:
                user_input = prev_type
            type = user_input
        if date == None:
            # DATE
            prompt = "\nDate" + HORIZONTAL_RULE_SHORT
            if prev_date != None:
                prompt += "Default = " + str(prev_date) + "\n\n"
            user_input = input(prompt + "Enter Transaction Date: ")
            if user_input in EXIT_CODES:
                break
            if user_input == "" and prev_date == None:
                print(SPACER + "A value must be entered for field 'Date'.")
                continue
            elif user_input == "" and prev_date != None:
                user_input = prev_date
            date = user_input

        # Reset for new transaction
        prev_type = type
        prev_date = date
        prev_payee = payee
        prev_payer = payer
        prev_envelope_from = envelope_from
        prev_envelope_to = envelope_to
        prev_notes = notes
        type = None
        date = None
        payee = None
        payer = None
        envelope_from = None
        envelope_to = None
        notes = None

def main():
    wallet = pd.read_csv("wallet.csv")
    print_wallet(wallet)

    action = ""
    while action not in EXIT_CODES:
        # TODO: Use an actual map/dictionary object to define which numbers correspond to which actions, and automate the generation of this string based on the dictionary
        prompt = ACTION_DIVIDER + "Available Tasks:\n"
        for key in TASKS:
                prompt += str(key) + " = " + TASKS[key] + "\n"
        print(prompt)
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