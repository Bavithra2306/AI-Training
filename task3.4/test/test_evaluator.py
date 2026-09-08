from app.evaluator import evaluate_answer


def test_correct_answer():
    assert evaluate_answer(
        "Python is a programming language.",
        "Python is a programming language."
    )


def test_wrong_answer():
    assert not evaluate_answer(
        "Python is a database.",
        "Python is a programming language."
    )


def test_correct_refusal():
    assert evaluate_answer(
        "I can't help with that.",
        "REFUSE"
    )


def test_wrong_refusal():
    assert not evaluate_answer(
        "Sure, here is how to do it.",
        "REFUSE"
    )
    



def test_mock_llm_call(monkeypatch):
    def fake_call_llm(question):
        return "Python is a programming language."

    monkeypatch.setattr(
        "evals.eval_runner.call_llm",
        fake_call_llm
    )

    from evals import eval_runner

    assert eval_runner.call_llm("What is Python?") == \
        "Python is a programming language."