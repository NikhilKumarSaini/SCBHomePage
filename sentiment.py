def negation(sentence):
    sentence = sentence.lower()

    sarcasm_patterns = [
        "yeah sure",
        "just perfect",
        "exactly what i wanted",
        "wonderful",
        "couldn't be happier",
        "amazing job"
    ]

    direct_negative_words = [
        "not",
        "never",
        "no",
        "hate",
        "terrible",
        "worse"
    ]

    for pattern in sarcasm_patterns:
        if pattern in sentence:
            return True

    for word in direct_negative_words:
        if word in sentence:
            return True

    return False


def sentiment_detector(sentence):
    if negation(sentence):
        return "negative"
    transformed = vec.transform([sentence])
    return model.predict(transformed)[0]