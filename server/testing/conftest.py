#!/usr/bin/env python3

import pytest
from app import app
from models import db, Article, User
from faker import Faker

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))

@pytest.fixture(scope='function')
def client():
    """Set up test client with seeded database."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        
        # Seed test data
        fake = Faker()
        
        users = [User(name=fake.name()) for i in range(3)]
        db.session.add_all(users)
        db.session.commit()
        
        articles = []
        for i in range(5):
            content = fake.paragraph(nb_sentences=8)
            preview = content[:25] + '...'
            
            article = Article(
                author=fake.name(),
                title=fake.sentence(),
                content=content,
                preview=preview,
                minutes_to_read=5,
                user_id=1
            )
            articles.append(article)
        
        db.session.add_all(articles)
        db.session.commit()
        
        yield app.test_client()
        
        db.session.remove()
        db.drop_all()

