
EXIT_CODES = ('X', 'x', 'exit', 'back')
ACTION_DIVIDER = "\n\n\n\n\n\n-----------------------------------\n\n"

def prompt_enter_txn():
    type = None
    date = None
    while True:
        print(ACTION_DIVIDER + "Enter Transaction Details:\nEnter 'X' for any field when finished entering transactions.\n")
        type = input("Type (1. Debit 2. Credit): ")
        if type in EXIT_CODES:
            break
        date = input("Date of Transaction: ")
        if date not in EXIT_CODES:
            break

def main():
    action = ""
    while action not in EXIT_CODES:
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