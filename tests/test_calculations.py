import pytest
from app.calculations import InsufficientFunds, add, div, mul, sub, BankAccount


@pytest.fixture
def bank_account_default():
    return BankAccount()

@pytest.fixture
def bank_account_initial():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (5, 3, 8),
    (5.5, 4.5, 10),
    (-10, 10, 0)
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected

def test_sub():
    print("testing sub function")
    assert sub(8, 4) == 4

def test_mul():
    print("testing mul function")
    assert mul(3, 3) == 9

def test_div():
    print("testing div function")
    assert div(18, 3) == 6


def test_bank_set_initial_amount(bank_account_initial):
    assert bank_account_initial.balance == 50

def test_bank_default_amount(bank_account_default):
    assert bank_account_default.balance == 0

def test_bank_withdraw_amount(bank_account_initial):
    bank_account_initial.withdraw(20)
    assert bank_account_initial.balance == 30 

def test_bank_deposit_amount(bank_account_initial):
    bank_account_initial.deposit(20)
    assert bank_account_initial.balance == 70 

def test_bank_collect_interest(bank_account_initial):
    bank_account_initial.collect_interest()
    assert round(bank_account_initial.balance, 6) == 55

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000),
])
def test_bank_transaction(bank_account_default, deposited, withdrew, expected):
    bank_account_default.deposit(deposited)
    bank_account_default.withdraw(withdrew)
    assert bank_account_default.balance == expected

def test_insufficient_funds(bank_account_default):
    with pytest.raises(InsufficientFunds):
        bank_account_default.withdraw(200)