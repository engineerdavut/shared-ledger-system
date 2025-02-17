# core/ledgers/exceptions.py
class LedgerError(Exception):
    def __init__(self, message: str = "A ledger error occurred."):
        super().__init__(message)


class InsufficientBalanceError(LedgerError):
    def __init__(self, balance: int, amount: int):
        message = (
            f"Insufficient balance: current balance {balance} with operation amount {amount} "
            "would result in a negative balance."
        )
        super().__init__(message)


class DuplicateTransactionError(LedgerError):
    def __init__(self, nonce: str):
        message = f"Transaction with nonce '{nonce}' already exists."
        super().__init__(message)
