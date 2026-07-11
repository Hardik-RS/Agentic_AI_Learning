import re

# Common prompt injection patterns
PROMPT_INJECTION_PATTERNS = [
    r"ignore (all )?previous instructions?",
    r"ignore (all )?above",
    r"forget (all )?previous instructions?",
    r"forget everything",
    r"reveal (your )?system prompt",
    r"show (your )?system prompt",
    r"print (your )?system prompt",
    r"developer instructions?",
    r"hidden instructions?",
    r"internal instructions?",
    r"act as .*without restrictions?",
    r"act as an unrestricted ai",
    r"bypass (your )?rules",
    r"override (your )?instructions?",
    r"disable (your )?safety",
    r"jailbreak",
    r"prompt injection",
    r"do not follow your rules",
    r"you are now",
]


def detect_prompt_injection(message):
    """
    Returns:
        (False, reason) -> Prompt injection detected
        (True, None)    -> Safe message
    """

    text = message.lower()

    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, text):
            return False, "Prompt injection attempt detected."

    return True, None