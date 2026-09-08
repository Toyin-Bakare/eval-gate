from eval_gate import Case
from eval_gate.scorers import format_validity, groundedness, task_completion


def test_task_completion():
    c = Case("1", "x", {"contains": ["foo", "bar"], "not_contains": ["baz"]})
    assert task_completion(c, "Foo and bar") == 1.0
    assert task_completion(c, "foo baz") == 1 / 3
    assert task_completion(Case("2", "x"), "anything") == 1.0


def test_format_json():
    c = Case("1", "x", {"format": "json", "required_keys": ["a", "b"]})
    assert format_validity(c, '{"a": 1, "b": 2}') == 1.0
    assert format_validity(c, '```json\n{"a": 1}\n```') == 0.5
    assert format_validity(c, "not json") == 0.0
    assert format_validity(Case("2", "x"), "not json") == 1.0


def test_groundedness():
    ctx = "The login endpoint returned 401 because the fixture token expired."
    c = Case("1", "x", context=ctx)
    assert groundedness(c, "The login endpoint returned 401 because the token expired.") == 1.0
    assert groundedness(c, "Mercury is the closest planet to the sun.") == 0.0
    assert groundedness(Case("2", "x"), "anything at all here") == 1.0
