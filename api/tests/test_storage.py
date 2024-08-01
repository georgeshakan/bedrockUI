

from agent.storage import Database
import os 

if not os.path.exists('history'):
    os.mkdir('history')

if os.path.exists('history/test.json'):
    os.remove('history/test.json')

def test_create_delete():
    
    db = Database()
    db.create('test')
    
    assert os.path.exists('history/test.json') == True
    db.delete('test')
    assert os.path.exists('history/test.json') == False

def test_create_error():
    db = Database()
    db.create('test')
    try:
        db.create('test')
    except ValueError as e:
        assert str(e) == 'Chat already exists'
    db.delete('test')

def test_read():
    db = Database()
    db.create('test')
    assert db.read('test') == []
    db.delete('test')

def test_put():
    db = Database()
    db.create('test')
    db.put('test', ['hello', 'world'])
    assert db.read('test') == ['hello', 'world']
    db.delete('test')

def test_append():
    db = Database()
    db.create('test')
    db.put('test', [{"message": "hello", "sender": "user"}])
    db.append('test', {"message": "world", "sender": "bot"})
    assert db.read('test') == [{"message": "hello", "sender": "user"}, {"message": "world", "sender": "bot"}]
    db.delete('test')