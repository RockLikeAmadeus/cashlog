
import numpy as np
import pandas as pd
from tabulate import tabulate

EXIT_CODES = ('X', 'x', 'exit', 'back')
ACTION_DIVIDER = "\n-----------------------------------\n\n"


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
    notes = None
    prompt = ""
    while True:
        print(ACTION_DIVIDER + "Enter Transaction Details:\nEnter 'X' for any field when finished entering transactions.\nPress return without entering a value into a field to use the value for that field specified in the previously entered transaction (excludes field 'Notes').\n")
        # TYPE
        # TODO: Use a dictionary/map for the number-type relationship here
        prompt = "Type\n----------\n1 = Debit\n2 = Credit\n"
        if prev_type != None:
            prompt += "Default = " + str(prev_type)
        type = input(prompt + "Enter Transaction Type: ")
        if type in EXIT_CODES:
            break
        if type == "" and prev_type == None:
            print("\nA value must be entered for field 'Type'.")
            continue
        elif type == "" and prev_type != None:
            type = prev_type
        prev_type = type
        # DATE

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
                prompt_enter_txn()
            case _:
                if action in EXIT_CODES:
                    continue
                print("\n\nPlease enter a number corresponding to the below listed available tasks. To exit, enter 'X'")

main()