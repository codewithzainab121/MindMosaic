CRISIS_KEYWORDS = [
    # English
    "suicide", "kill myself", "end my life", "want to die", "self harm",
    "hurt myself", "no reason to live", "give up", "hopeless", "worthless",
    # Urdu
    "khud ko maar", "zindagi khatam", "marna chahta", "marna chahti",
    "jeena nahi", "khatam karna", "bardasht nahi", "takleef", "dard"
]

STRESS_KEYWORDS = [
    # English
    "stress", "anxiety", "worried", "panic", "overwhelmed",
    "nervous", "depressed", "sad", "lonely", "scared", "frustrated",
    # Urdu 
    "pareshan", "udaas", "ghabrahat", "tanha", "akela", "akeli",
    "dara", "fikar", "tension", "mushkil", "mushkilaat"
]

def detect_crisis(message: str) -> bool:
    msg = message.lower()
    return any(kw in msg for kw in CRISIS_KEYWORDS)

def detect_stress(message: str) -> bool:
    msg = message.lower()
    return any(kw in msg for kw in STRESS_KEYWORDS)

def get_crisis_response() -> str:
    return (
        "⚠️ I'm genuinely concerned about you right now. "
        "Please reach out to a crisis helpline immediately.\n\n"
        "🇵🇰 Pakistan: helpline — 0800-99000\n"
        "🌍 International: findahelpline.com\n\n"
        "You are not alone. Please talk to someone you trust. 💙"
    )
