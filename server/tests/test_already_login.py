# from datetime import datetime

# def compute_interest_rate_for_affirm_loan(loan_amount, loan_start_date, loan_end_date, total_interest_amount):
#     start_date = datetime.strptime(loan_start_date, "%m/%d/%y")
#     end_date = datetime.strptime(loan_end_date, "%m/%d/%y")
#     loan_period_days = (end_date - start_date).days
#     interest_rate = total_interest_amount / (loan_amount * (loan_period_days / 365))
#     return round(interest_rate, 2)

# # Test Cases
# test_cases = [
#     (6700, "03/05/22", "07/10/22", 450),
#     (10000, "01/01/22", "12/31/22", 1000)
# ]

# # Testing the function with the provided test cases
# for loan_amount, start_date, end_date, interest_amount in test_cases:
#     interest_rate = compute_interest_rate_for_affirm_loan(loan_amount, start_date, end_date, interest_amount)
#     print(f"Loan Amount: {loan_amount}, Start Date: {start_date}, End Date: {end_date}, Interest Amount: {interest_amount}, Interest Rate: {interest_rate}")

# 2. Affirm Interest Rates
# Affirm provides millions of loans each day. Customers can also choose between multiple payment options at checkout, with differing repayment schedules that can differ in interest rates.
# We show these options to our customers before they pay, along with the total payment amount for their loan, interest included. Here is the formula for an annualized interest rate:
# R= I/(P * (t/365))
# Where:
# R = the interest rate for the loan (rounded to two decimal places)
# | = The total interest amount accrued for the loan (in cents)
# P = The principal amount for the loan, without interest (in cents)
# t = The total time period of the loan (in days)
# Total interest amount is a specified finance charge that Affirm sets for each loan. We can also change this amount under certain circumstances. In this problem, you will write one method to implement loan interest logic.
# Write a method called compute interest_rate _for_affirm_ loan that accepts the following parameters:
# loan_amount, of type int, a positive integer which represents the principal loan amount in cents (Ex: 6700 = $67.00).
# loan start date, of type string, which represents the starting date for the loan, and the starting time period for interest accrual. This value will be passed in the following format %MM/%DD/%YY (ex: 03/05/22).
# loan end date, of type string, which represents the ending date for the loan, and the end of the time period for interest accrual. This value will be passed in the following format %MM/%DD/%YY (ex: 07/10/22).
# total interest amount, of type int, a non-negative integer which represents the total interest amount in cents (ex: 450 = $4.50).
# You'll be implementing this method to calculate the interest rates for a given loan of a specified number of days. The total number of days in the loan will be the days between loan start_date and loan_end _date.
# base
# A year is divided into 12 months in the modern-day Gregorian calendar. The months are either 28, 29, 30, or 31 days long.
# The Gregorian calendar consists of the following 12 months:
# 1.    January - 31 days
# 2.    February - 28 days in a common year (we are ignoring leap years for this problem)
# 3.    March - 31 days
# 4.    April - 30 days
# 5.    May - 31 days
# 6.    June - 30 days
# 7.    July - 31 days
# 8.    August - 31 days
# 9.    September - 30 days
# 10.  October - 31 days
# 11.     November - 30 days
# 12.     December - 31 days
# For the given test cases:
# -   loan _amount will not exceed 30,000.
# -   total interest_ amount will not exceed 10,000.
# -   the months in both loan start_date and loan end_date will range from 01-12.
# -   the days in both loan_start date and loan end date will range from 01-31.
# -   the year in both loan start date and loan end date will range from 01-31.
# -   all loans will start in the same calendar year they end in.


# from datetime import datetime

# def compute_interest_rate_for_affirm_loan(loan_amount, loan_start_date, loan_end_date, total_interest_amount):
#     if loan_amount <= 0:
#         return -1.0  # Invalid loan amount
#     if not is_valid_date(loan_start_date) or not is_valid_date(loan_end_date):
#         return -1.0  # Invalid loan start or end dates
#     start_date = datetime.strptime(loan_start_date, "%m/%d/%y")
#     end_date = datetime.strptime(loan_end_date, "%m/%d/%y")
#     if start_date > end_date:
#         return -1.0  # Invalid start date after end date
#     time_period = (end_date - start_date).days
#     if total_interest_amount < 0:
#         return -1.0  # Invalid total interest amount
#     interest_rate = total_interest_amount / (loan_amount * (time_period / 365.0))
#     interest_rate = round(interest_rate, 2)
#     return interest_rate
#     # except ValueError:
#     #     return -1.0  # Invalid date format

# def is_valid_date(date_str):
#     try:
#         datetime.strptime(date_str, "%m/%d/%y")
#         return True
#     except ValueError:
#         return False

# # Example usage
# loan_amount = 1000
# loan_start_date = "03/05/22"
# loan_end_date = "07/10/22"
# total_interest_amount = 400

# interest_rate = compute_interest_rate_for_affirm_loan(loan_amount, loan_start_date, loan_end_date, total_interest_amount)
# print(interest_rate)

def most_over_captured(lines):
    card_to_capture_amount = {}

    current_card = 0

    for line in lines:
        tokens = line.split()
        amount = int(tokens[-1])

        if "CARD #" in line:
            current_card = int(tokens[-3])
        elif "CAPTURE" in line:
            card_to_capture_amount[current_card] = card_to_capture_amount.get(current_card, 0) + amount

    max_card = -1
    max_capture_amount = -1

    for card, capture_amount in card_to_capture_amount.items():
        if capture_amount > max_capture_amount:
            max_capture_amount = capture_amount
            max_card = card

    if max_card != -1:
        print("TIMING CARD:", max_card, "2")  # Unsure why "2" is printed here, might be an error in original Java code
        print("OVERCAPTURED CARD:", max_card, max_capture_amount)
    else:
        print("TIMING CARD: -1 -1")
        print("No card exists.")

def most_negative_captures(lines):
    card_to_negative_captures = {}

    current_card = 0

    for line in lines:
        tokens = line.split()
        amount = int(tokens[-1])

        if "CARD #" in line:
            current_card = int(tokens[-3])
        elif "CAPTURE" in line and amount < 0:
            card_to_negative_captures[current_card] = card_to_negative_captures.get(current_card, 0) + 1

    max_card = -1
    max_negative_captures = -1

    for card, negative_captures in card_to_negative_captures.items():
        if negative_captures > max_negative_captures:
            max_negative_captures = negative_captures
            max_card = card

    if max_card != -1:
        print("NEGATIVE CARD:", max_card, max_negative_captures)
    else:
        print("NEGATIVE CARD: -1 -1")

# Sample input
# lines = [
#     "[2020 11 01 23:58] CARD # 98 AUTH 100",
#     "[2020 11 02 00:40] CAPTURE 50",
#     "[2020-11-03 00:05] CARD # 17 AUTH 100",
#     "[2020 11 03 00:24] CAPTURE 50",
#     "[2020-11-05 00:03] CARD # 90 AUTH 200",
#     "[2020 11 05 00:45] CAPTURE 34",
#     "[2020 11 01 00:01] CARD # 10 AUTH 300",
#     "[2020-11-01 00:05] CAPTURE 300",
#     "[2020 11 01 00:30] CAPTURE 200",
#     "[2020 11-04 00:02] CARD # 97 AUTH 400",
#     "[2020 11-04 00:36] CAPTURE 30"
# ]

from datetime import datetime

def find_suspect_users(events):
    cards = {}
    for event in events:
        time, event_type, *details = event.split()
        time = datetime.strptime(time, '[%Y-%m-%d %H:%M]')
        if event_type.lower() == 'card':
            card_num, _, amount = details
            if card_num not in cards:
                cards[card_num] = {'auth_amount': int(amount), 'captures': [], 'negative_captures': 0}
            else:
                cards[card_num]['auth_amount'] += int(amount)
        elif event_type.lower() == 'capture':
            amount = int(details[0])
            if amount &lt; 0:
                cards[card_num]['negative_captures'] += 1
            else:
                cards[card_num]['captures'].append((time, amount))

    suspect_cards = {'most_non_active_captures': ('', 0), 'largest_captured_amount': ('', 0), 'most_negative_captures': ('', 0)}
    for card_num, card_info in cards.items():
        non_active_captures = sum(1 for time, _ in card_info['captures'] if time.hour &lt; 8 or time.hour &gt;= 22)
        if non_active_captures &gt; suspect_cards['most_non_active_captures'][1]:
            suspect_cards['most_non_active_captures'] = (card_num, non_active_captures)
        total_captured_amount = sum(amount for _, amount in card_info['captures'])
        if total_captured_amount &gt; suspect_cards['largest_captured_amount'][1]:
            suspect_cards['largest_captured_amount'] = (card_num, total_captured_amount)
        if card_info['negative_captures'] &gt; suspect_cards['most_negative_captures'][1]:
            suspect_cards['most_negative_captures'] = (card_num, card_info['negative_captures'])

    return suspect_cards

lines = [
    "[2020 11 01 23:58] CARD # 98 AUTH 100",
    "[2020 11 02 00:40] CAPTURE 100"
]

# Run the analysis
# most_over_captured(lines)
# most_negative_captures(lines)
print(find_suspect_users(lines))
