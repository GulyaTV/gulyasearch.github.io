# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser

app = Flask(__name__)

# Создаем схему для индекса
schema = Schema(content=TEXT)
index = create_in("indexdir", schema)

# Добавляем некоторые документы в индекс
writer = index.writer()
writer.add_document(content="This is the content of document 1.")
writer.add_document(content="This is the content of document 2.")
writer.commit()

# Определяем маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Определяем маршрут для обработки поискового запроса
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    searcher = index.searcher()
    query_parser = QueryParser("content", index.schema)
    parsed_query = query_parser.parse(query)
    results = searcher.search(parsed_query)
    searcher.close()
    return render_template('search_results.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)