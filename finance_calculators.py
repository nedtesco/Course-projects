import math

valid_response = False

# Creating a loop that will continue to prompt the user for input until a
# valid response is provided.
while valid_response == False:
    finance_option = input("""investment - to calculate the amount of interest you'll earn on your investment
bond - to calculate the amount you'll have to pay on a home loan
Enter either 'investment' or 'bond' from the menu above to proceed:
> """).lower()

    # If user chooses 'investment', they will be asked to enter a set of variables
    # to be calculated, as well as what type of interest which will dictate the nature
    # of the calculation
    if finance_option == "investment":
        valid_response = True
        deposit = int(input("Please enter your deposit amount (in dollars): "))
        rate = float(input("Please enter the enterest rate (as a %): ")) / 100
        years_invested = int(input("How many years do you plan on investing? "))
        interest = input("Would you like simple or compound interest? Please enter simple or compound: ").lower()

        if interest == "simple":
            investment_result = deposit * (1 + rate * years_invested)

        elif interest == "compound":
            investment_result = deposit * math.pow((1 + rate), years_invested)

        print(f"Total amount after investment: ${investment_result}")

    # If user chooses 'bond', they will be asked to enter a different set of variables
    # to be calculated.
    elif finance_option == "bond":
        valid_response = True
        value = int(input("Please enter the value of your home (in $): "))
        rate = float(input("Please enter the enterest rate (as a %): ")) / 100 / 12
        months_invested = int(input("How many months do you plan to take to repay the bond? "))
        bond_repayment = (rate * value) / (1 - (1 + rate)**(-months_invested))

        print(f"Monthly repayment amount: ${bond_repayment}")

    # User told if input is invalid and allowed to re-enter a response.
    else:
        print("Error - Please enter a valid response.")
