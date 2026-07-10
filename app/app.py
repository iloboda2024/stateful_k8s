from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask-user:flask-password@postgres.postgres.svc.cluster.local:5432/flask-db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80),nullable=False)
    description = db.Column(db.String(200))

@app.route('/tasks',methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify({
        'tasks': [{ 
            'id': task.id, 
            'title': task.title, 
            'description': task.description
        } for task in tasks ]
    })

@app.route('/tasks',methods=['POST'])
def add_task():
    data = request.get_json()
    title = data['title']
    description = data['description']
    task = Task(title=title,description=description)
    db.session.add(task)
    db.session.commit()
    return jsonify({'task': {
        'id': task.id,
        'title': task.title,
        'description': task.description
    }})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)

#curl -X POST -H "Content-Type: application/json" -d '{"title": "Learn Flask", "description": "First task"}' http://127.0.0.1:5000/tasks

