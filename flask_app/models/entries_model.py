from html import entities
import queue
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Entry:
    db = "entries"
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.title = data['title']
        self.description = data['description']
        self.mood = data['mood']
        self.journal = data['journal']

    @classmethod
    def create(cls, data):
        query = "INSERT into entries (title, description, mood, journal) VALUES (%(title)s,%(description)s,%(mood)s,%(journal)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM entries WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if results:
            return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM entries;"
        results = connectToMySQL(cls.db).query_db(query)
        entries = []
        for entry in results: 
            entries.append(cls(entry))
        return entries

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM entries WHERE id = %(id)s;"
        return connectToMySQL('entries').query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE entries SET description=%(description)s, mood=%(mood)s,journal=%(journal)s, updated_at=NOW()WHERE id = %(id)s;"
        return connectToMySQL('entries').query_db(query,data)

    @classmethod
    def join(cls):
        query="SELECT * FROM entries LEFT JOIN USERS ON entries.users_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        entrier = []
        for entriers in results:
            entrier.append(cls(entriers))
        return entrier

    @staticmethod
    def is_valid_journal(entries):
        print(entries)
        is_valid = True
        if len(entries['title']) < 1:
            is_valid = False
            flash("Must have a Title.", "create_entries")
        if len(entries['description']) < 20:
            is_valid = False
            flash("Must have a brief description", 'create_entries')
        if len(entries['mood']) < 20:
            is_valid = False
            flash("Must have an associated mood", 'create_entries')
        if len(entries['journal']) < 1:
            is_valid = False
            flash("Have text", 'create_entries')
        return is_valid 
