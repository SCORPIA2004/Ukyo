# app.py
from itertools import combinations
from allpairspy import AllPairs
from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

def generate_pairwise_tests(parameters):
    """
    Generates pairwise test cases and calculates unique pairs.
    :param parameters: Dictionary of parameter groups and their values.
    :return: List of test cases and the count of unique pairs per test case.
    """
    param_names = list(parameters.keys())
    param_values = list(parameters.values())
    
    pairwise_cases = list(AllPairs(param_values))
    
    all_unique_pairs = set()
    test_case_unique_pair_counts = []
    
    for case in pairwise_cases:
        case_pairs = set(combinations(case, 2))
        test_case_unique_pair_counts.append(len(case_pairs - all_unique_pairs))
        all_unique_pairs.update(case_pairs)
    
    return pairwise_cases, test_case_unique_pair_counts, all_unique_pairs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    parameters = data.get("parameters", {})
    if not parameters:
        return jsonify({"error": "No parameters provided"}), 400
    
    test_cases, unique_pair_counts, all_unique_pairs = generate_pairwise_tests(parameters)
    
    results = []
    for i, (case, unique_count) in enumerate(zip(test_cases, unique_pair_counts), 1):
        results.append({"Test Case #": i, **dict(zip(parameters.keys(), case))})
        results[-1]["# Unique Pairs"] = unique_count
    
    return jsonify({"test_cases": results, "total_test_cases": len(test_cases), "total_unique_pairs": len(all_unique_pairs)})

def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()