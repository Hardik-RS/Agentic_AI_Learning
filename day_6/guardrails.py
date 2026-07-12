MAX_LENGTH = 3000

BLOCKED_PHRASES = [
    "ignore previous instructions",
    "reveal system prompt",
    "developer instructions",
    "show hidden prompt"
]

def validate_input(message):
    if not isinstance(message, str):
        return False, "Invalid message."

    message = message.strip()

    if not message:
        return False, "Message cannot be empty."

    if len(message) > MAX_LENGTH:
        return False, "Message is too long."

    lower = message.lower()

    for phrase in BLOCKED_PHRASES:
        if phrase in lower:
            return False, "I can't comply with that request."

    return True, message