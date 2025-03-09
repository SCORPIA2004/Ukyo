from itertools import combinations
from allpairspy import AllPairs
from tabulate import tabulate

def generate_pairwise_tests(parameters):
    """
    Generates pairwise test cases and calculates unique pairs.
    :param parameters: Dictionary of parameter groups and their values.
    :return: List of test cases and the count of unique pairs per test case.
    """
    param_names = list(parameters.keys())
    param_values = list(parameters.values())
    
    # Generate pairwise test cases using allpairspy
    pairwise_cases = list(AllPairs(param_values))
    
    # Collect all unique pairs across all test cases
    all_unique_pairs = set()
    test_case_unique_pair_counts = []
    
    for case in pairwise_cases:
        case_pairs = set(combinations(case, 2))  # Unique pairs within the test case
        test_case_unique_pair_counts.append(len(case_pairs - all_unique_pairs))
        all_unique_pairs.update(case_pairs)
    
    return pairwise_cases, test_case_unique_pair_counts, all_unique_pairs

# Define parameters
parameters = {
    "Browser": ["Chrome", "Firefox", "Edge"],
    "Auth Method": ["Password", "OTP", "SMS", "Biometric"],
    "User Type": ["Admin", "Guest", "Staff"],
    "Environment": ["Dev", "Staging", "Prod", "Local"],
    "OS": ["Windows", "Linux", "Mac"]
}

# Generate test cases and unique pairs
test_cases, unique_pair_counts, all_unique_pairs = generate_pairwise_tests(parameters)

# Prepare table data
table_data = []
for i, (case, unique_count) in enumerate(zip(test_cases, unique_pair_counts), 1):
    row = [i] + list(case) + [unique_count]
    table_data.append(row)

# Define table headers
headers = ["Test Case #"] + list(parameters.keys()) + ["# of New Unique Pairs Introduced"]

# Print results in table format
print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Print total number of test cases
print(f"\nTotal Number of Test Cases: {len(test_cases)}")

# Print total unique pairs
print(f"\nTotal Unique Pairs Across All Test Cases: {len(all_unique_pairs)}")