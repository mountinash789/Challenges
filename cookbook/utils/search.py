from django.db.models import Sum

from nltk.stem import PorterStemmer


def generate_keywords(text):
    stemmer = PorterStemmer()
    tokens = [s.lower() for s in text.split()]

    tokens = [''.join(c for c in token if c.isalpha()) for token in tokens]

    words = []
    other = []
    for token in tokens:
        (other if any(s.isdigit() for s in token) else words).append(token)

    words = [stemmer.stem(w) for w in words]

    tokens = set(t[:50] for t in words + other if t)

    return tokens


def search(query, qs):
    keywords = generate_keywords(query)
    recipes = qs.filter(
        keyword__keyword__in=keywords,
    ).annotate(
        search_score=Sum('keyword__importance'),
    ).order_by(
        '-search_score',
    )

    return recipes
