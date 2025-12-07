from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_courses(user_goal, user_skills, courses):
    # Chuẩn bị data
    docs = []
    for c in courses:
        combined_text = (
            c.get("title", "") + " " +
            c.get("description", "") + " " +
            " ".join(c.get("skills_required", [])) + " " +
            c.get("category", "")
        )
        docs.append(combined_text)

    # User input
    user_text = user_goal + " " + " ".join(user_skills)

    docs.append(user_text)

    # Vector TF-IDF
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(docs)

    # Tính similarity score
    user_vector = vectors[-1]
    course_vectors = vectors[:-1]

    similarities = cosine_similarity(user_vector, course_vectors).flatten()

    # Lấy danh sách chỉ số sắp xếp theo độ phù hợp (descending)
    sorted_indexes = similarities.argsort()[::-1]

    return sorted_indexes, similarities
