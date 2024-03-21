#TO RUN TESTS
# in the main directory ( FastApiTutorial)
# pytest -v -s --disable-warnings -x
# -v for verbose , -s for printing print statement, --disable warnings if you want to , -x to stop at first failure

import pytest
from app.calculations import add, subtract, multiply, divide, InsufficientFunds, BankAccount

#----1.FIXTURES--------------------------------------------------------------------------------------------------

@pytest.fixture
def zero_bank_account():
    print("Creating an Empty Bank account")
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(77)

#----2.PARAMETERS---------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("num1, num2, expected",[
    (3,2,5),
    (-2,1,-1),
    (-8,-3,-11)                  
])

#----3.TESTS---------------------------------------------------------------------------------------------------------

#---3.1 Using Parameters---
def test_add(num1, num2, expected):
    assert expected == add(num1,num2)

#---3.2 Using Fixtures---
def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 77


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 57


def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 107


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 0) == 85

#---3.3 Fixtures + Parameters---
    
@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000),
])

def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

@pytest.mark.parametrize("deposited,withdrew",[
    (10,20),
])

def test_insufficient_funds(zero_bank_account,deposited,withdrew):
    zero_bank_account.deposit(deposited)
    with pytest.raises(InsufficientFunds):
        zero_bank_account.withdraw(withdrew)