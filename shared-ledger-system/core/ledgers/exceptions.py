# core/ledgers/exceptions.py

class LedgerError(Exception):
    """Ledger ile ilgili genel hata sınıfı."""
    def __init__(self, message: str = "A ledger error occurred."):
        super().__init__(message)

class InsufficientBalanceError(LedgerError):
    """Ledger işlemi sonucunda negatif bakiye oluşacaksa bu hatayı fırlatır."""
    def __init__(self, balance: int, amount: int):
        message = (f"Insufficient balance: current balance {balance} with operation amount {amount} "
                   "would result in a negative balance.")
        super().__init__(message)

class DuplicateTransactionError(LedgerError):
    """Aynı nonce değeriyle yapılan işlemlerde tekrarı engellemek için kullanılır."""
    def __init__(self, nonce: str):
        message = f"Transaction with nonce '{nonce}' already exists."
        super().__init__(message)