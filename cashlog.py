
import numpy as np
import pandas as pd
from tabulate import tabulate
from register_transaction import register_transaction

EXIT_CODES = ('X', 'x', 'exit', 'back')
SPACER = "\n\n\n\n\n\n"
HORIZONTAL_RULE_SHORT = "\n----------\n"
HORIZONTAL_RULE_LONG = "\n-----------------------------------\n"

# Enumerations
TASKS = { 
    1: "Enter a transaction",
    2: "Allocate funds based on a pre-configured distribution",
    3: "Transfer funds between envelope",
    4: "View your wallet",
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
    amount, prev_amount = None, None
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
                print(SPACER)
                return
            if user_input == "" and prev_type == None:
                print(SPACER + "A value must be entered for field 'Type'.")
                continue
            elif user_input == "" and prev_type != None:
                type = prev_type
            else:
                type = TRANSACTION_TYPE[int(user_input)]
        if date == None:
            # DATE
            prompt = "\nDate" + HORIZONTAL_RULE_SHORT
            if prev_date != None:
                prompt += "Default = " + str(prev_date) + "\n\n"
            user_input = input(prompt + "Enter Transaction Date: ")
            if user_input in EXIT_CODES:
                print(SPACER)
                return
            if user_input == "" and prev_date == None:
                print(SPACER + "A value must be entered for field 'Date'.")
                continue
            elif user_input == "" and prev_date != None:
                user_input = prev_date
            date = user_input
        match type:
            case "Debit":
                if payee == None:
                    # Payee
                    prompt = "\nPayee" + HORIZONTAL_RULE_SHORT
                    if prev_payee != None:
                        prompt += "Default = " + str(prev_payee) + "\n\n"
                    user_input = input(prompt + "Enter Payee: ")
                    if user_input in EXIT_CODES:
                        print(SPACER)
                        return
                    if user_input == "" and prev_payee == None:
                        print(SPACER + "A value must be entered for field 'Payee'.")
                        continue
                    elif user_input == "" and prev_payee != None:
                        user_input = prev_payee
                    payee = user_input
                    payer = ""
            case "Credit":
                if payer == None:
                    # Payer
                    prompt = "\nPayer" + HORIZONTAL_RULE_SHORT
                    if prev_payer != None:
                        prompt += "Default = " + str(prev_payer) + "\n\n"
                    user_input = input(prompt + "Enter Payer: ")
                    if user_input in EXIT_CODES:
                        print(SPACER)
                        return
                    if user_input == "" and prev_payer == None:
                        print(SPACER + "A value must be entered for field 'Payer'.")
                        continue
                    elif user_input == "" and prev_payer != None:
                        user_input = prev_payer
                    payer = user_input
                    payee = ""
        if amount == None:
            # AMOUNT
            prompt = "\nAmount" + HORIZONTAL_RULE_SHORT
            if prev_amount != None:
                prompt += "Default = " + str(prev_amount) + "\n\n"
            user_input = input(prompt + "Enter Transaction Amount: ")
            if user_input in EXIT_CODES:
                print(SPACER)
                return
            if user_input == "" and prev_amount == None:
                print(SPACER + "A value must be entered for field 'Amount'.")
                continue
            elif user_input == "" and prev_amount != None:
                user_input = prev_amount
            amount = float(user_input)
        match type:
            case "Debit":
                if envelope_from == None:
                    # From Envelope
                    prompt = "\nEnvelope" + HORIZONTAL_RULE_SHORT
                    if prev_envelope_from != None:
                        prompt += "Default = " + str(prev_envelope_from) + "\n\n"
                    user_input = input(prompt + "Deduct From Envelope: ")
                    if user_input in EXIT_CODES:
                        print(SPACER)
                        return
                    if user_input == "" and prev_envelope_from == None:
                        print(SPACER + "You must specify an envelope from which to draw.")
                        continue
                    elif user_input == "" and prev_envelope_from != None:
                        user_input = prev_envelope_from
                    # TODO: if envelope_from not in envelopes
                    envelope_from = user_input
                    envelope_to = ""
            case "Credit":
                envelope_from = ""
                envelope_to = "Unallocated"
        # Notes
        prompt = "\nNotes" + HORIZONTAL_RULE_SHORT
        user_input = input(prompt + "Enter Transaction Notes: ")
        if user_input in EXIT_CODES:
            print(SPACER)
            return
        notes = user_input

        # Confirmation
        print(SPACER)
        print("Transaction Details:")
        print(HORIZONTAL_RULE_LONG)
        print("Type: " + type)
        print("Date: " + date)
        match type:
            case "Debit":
                print("Payee: " + payee)
            case "Credit":
                print("Payer: " + payer)
        print("Amount: " + str(amount))
        if type == "Debit":
            print("Deduct From: " + envelope_from)
        if notes != "":
            print("Notes: " + notes)
        print(HORIZONTAL_RULE_LONG)
        confirmation = input("Press Enter to confirm. Enter 'X' and press Enter to cancel: ")

        if confirmation == "":
            # Call enter transaction function from different file here. This file will not reference pandas or the CSV directly.
            match type:
                case "Debit":
                    register_transaction(date, type, payee, amount, None, None, notes)
                case "Credit":
                    register_transaction(date, type, payer, amount, None, None, notes)

        # If anything but the empty string is entered, do not confirm transaction entry.
        # Reset for new transaction, whether current transaction was entered or cancelled
        prev_type = type
        prev_date = date
        prev_payee = payee
        prev_payer = payer
        prev_amount = amount
        prev_envelope_from = envelope_from
        prev_envelope_to = envelope_to
        prev_notes = notes
        type = None
        date = None
        payee = None
        payer = None
        amount = None
        envelope_from = None
        envelope_to = None
        notes = None

def main():
    wallet = pd.read_csv("wallet.csv")
    print_wallet(wallet)
    print(SPACER)

    action = ""
    while True:
        # TODO: Use an actual map/dictionary object to define which numbers correspond to which actions, and automate the generation of this string based on the dictionary
        prompt = "Available Tasks:" + HORIZONTAL_RULE_LONG
        for key in TASKS:
                prompt += str(key) + " = " + TASKS[key] + "\n"
        print(prompt)
        action = input("Choose a task: ")
        match action:
            case "1":
                print(SPACER)
                prompt_enter_txn()
            case "4":
                print(SPACER)
                print_wallet(wallet)
                print(HORIZONTAL_RULE_SHORT)
            case _:
                if action in EXIT_CODES:
                    print(SPACER)
                    return
                print(SPACER + "Please enter a number corresponding to the below listed available tasks. To exit, enter 'X'\n")

main()