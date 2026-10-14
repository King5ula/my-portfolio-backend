from app.prompts.david_prompt import DAVID_PROMPT


def test_prompt_includes_project_facts_and_guardrails():
    for project in ("Turners Cars", "Tina", "Z Energy", "purpOS"):
        assert project in DAVID_PROMPT
    assert "Never invent" in DAVID_PROMPT
    assert "plain text only" in DAVID_PROMPT
    assert "Diploma in Advanced AI-Powered Full-Stack Development" in DAVID_PROMPT
