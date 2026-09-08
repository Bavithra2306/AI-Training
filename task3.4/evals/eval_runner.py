import json

from app.llm import call_llm
from app.evaluator import evaluate_answer


def run_evaluation():
    with open("evals/golden_set.json", "r") as file:
        golden_set = json.load(file)

    passed = 0
    failed = 0

    for case in golden_set:
        question = case["question"]
        expected = case["expected"]

        try:
            actual = call_llm(question)
            result = evaluate_answer(actual, expected)

        except Exception as e:
            print(f"Case {case['id']}: ERROR - {type(e).__name__}")
            continue

        if result:
            passed += 1
            print(f"Case {case['id']}: PASS")
        else:
            failed += 1
            print(f"Case {case['id']}: FAIL")

    completed = passed + failed

    print("\n====================")
    print(f"Passed: {passed}/{completed}")
    print(f"Failed: {failed}/{completed}")

    if completed:
        pass_rate = (passed / completed) * 100
        print(f"Pass rate: {pass_rate:.0f}%")
    else:
        print("Pass rate: N/A")

    print("====================")


if __name__ == "__main__":
    run_evaluation()