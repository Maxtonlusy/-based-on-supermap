import jieba
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from . import tool
from flask import Blueprint ,jsonify,request
nlp= Blueprint('nlp', __name__, url_prefix='/nlp')
@nlp.route('/nlp', methods=[ 'GET'])
def feedback():
    def get_db_data(database, chart_name, column):
        connection = tool.get_db_connection(database)
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT {column} FROM {chart_name}"
        cursor.execute(query, )
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data

    feeddata = get_db_data('feedback', 'user_feedback', 'content')
    list_ = []
    for i in feeddata:
        list_.append(i['content'])
    print(list_)
    print(feeddata)
    user_feedback = list_

    def preprocess_text(text):
        # 分词
        words = jieba.lcut(text)

        stop_words = {"的", "都", "要", "很", "但", "了", "有", "能否", "希望", "每次", "试了", "好几次", "有点", "太",
                      "比"}
        filtered_words = [word for word in words if word not in stop_words and not word.isdigit() and len(word) > 1]

        return " ".join(filtered_words)

    processed_feedback = [preprocess_text(feedback) for feedback in user_feedback]

    tfidf = TfidfVectorizer()

    tfidf_matrix = tfidf.fit_transform(processed_feedback)

    vocab = tfidf.get_feature_names_out()

    total_tfidf = np.sum(tfidf_matrix.toarray(), axis=0)


    word_value_dict = dict(zip(vocab, total_tfidf))

    sorted_word_value = sorted(word_value_dict.items(), key=lambda x: x[1], reverse=True)[:10]

    dict_feedback = {}
    for i, (word, value) in enumerate(sorted_word_value, 1):
        dict_feedback[word] = value
    return dict_feedback
