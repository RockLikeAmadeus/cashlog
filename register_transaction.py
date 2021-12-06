import numpy as np
import pandas as pd
import os

from os.path import exists

# Find a place to put stuff like this in its own file
LEDGER_FILE = 'ledger.csv'
LEDGER_COLUMNS = ['date', 'type', 'target', 'deduct_from_envelope', 'add_to_envelope', 'account', 'notes']

def register_transaction(date, type, target, deduct_from, add_to, account, notes):
    transaction = [[date, type, target, deduct_from, add_to, account, notes]]
    df = pd.DataFrame(transaction, columns = LEDGER_COLUMNS)
    if not exists(LEDGER_FILE):
        df.to_csv(LEDGER_FILE, index=False)
    else:
        df.to_csv(LEDGER_FILE, mode='a', index=False, header=False)

    #TODO: adjust wallet to reflect entered transaction