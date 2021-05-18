from flask import Flask ,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db.Integer,default=0)
    date_created = db.Column(db.DateTime,default =datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/",methods=['POST','GET'])
def index():
    if request.method=='POST':
        taskContent = request.form['content']
        newContent = Todo(content=taskContent)

        try:
            db.session.add(newContent)
            db.session.commit()
            return redirect("/")

        except:
            return 'There was an issue with adding the task'  

    else:  
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)

if __name__=="__main__":
    app.run(debug=True)    
