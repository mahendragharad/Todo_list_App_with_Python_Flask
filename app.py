from flask import Flask, render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from flask import flash
from datetime import datetime
from logger import logging
from exception import CustomException
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///My_todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    try :
        logging.info("Creating Schema To Save Todo's")
        Sr_No = db.Column(db.Integer, primary_key=True )
        task_desc = db.Column(db.String(200), nullable=False)
        priority = db.Column(db.String(20), nullable=False)
        due_date = db.Column(db.DateTime, default=datetime.utcnow)
        category = db.Column(db.String(50), nullable=False)
        dependencies = db.Column(db.String(20), nullable=False)
        estimated_time = db.Column(db.String(20), nullable=False)
        progress = db.Column(db.String(20), nullable=False)
        completion_reward = db.Column(db.String(20), nullable=False)
    except Exception as e :
        logging.info("Error Occured during schema creation")
        raise CustomException(e)

    def __repr__(self) -> str:
        try :
            logging.info("returning task description to test class")
            return f"{self.task_desc} - {self.priority}"
        except Exception as e :
            logging.info("error Occured in Todo Class")
            raise CustomException(e)

    
@app.route('/' , methods=['GET' , 'POST']) 
def put_data() :
    try :
        logging.info("Inside Route Put Data")
        logging.info("Trying to post data to the form")

        if request.method=='POST' :
            logging.info("Making Post Method")
            task_desc=request.form['taskDescription']
            priority=request.form['priority']
            due_date=request.form['dueDate']
            category=request.form['category']
            dependencies=request.form['dependencies']
            estimated_time=request.form['estimatedTime']
            progress=request.form['progress']
            completion_reward=request.form['reward']

            logging.info("Data Posted")
            todo = Todo( task_desc=task_desc , priority=priority , category=category , dependencies=dependencies , estimated_time=estimated_time, progress=progress , completion_reward=completion_reward)

            logging.info("Data Added Successfully")
            db.session.add(todo)
            db.session.commit()

            # flash('You have submitted your todo!', 'success')

        allTodo = Todo.query.all()
        return render_template('index.html' , allTodo=allTodo)
    
    except Exception as e :
        logging.info("error Occured During Data submission")
        raise CustomException(e)

@app.route('/todo-list')
def todo_list():
    try :
        logging.info("Inside Todo-List route")
        allTodo = Todo.query.all()
        return render_template('my_todos.html', allTodo=allTodo) 
    except Exception as e :
        logging.info("Error Occured During Printing data to the table.html page")
        raise CustomException(e)


@app.route('/update/<int:Sr_No>', methods=['GET', 'POST'])
def update(Sr_No):
    try :
        logging.info("Inside Update Route")
        if request.method == 'POST':
            task_desc = request.form['taskDescription']
            priority = request.form['priority']
            due_date_str = request.form['dueDate']  # Get due date as string from form input
            category = request.form['category']
            dependencies = request.form['dependencies']
            estimated_time = request.form['estimatedTime']
            progress = request.form['progress']
            completion_reward = request.form['reward']

            logging.info("Convert due_date_str to datetime object")
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()

            logging.info("filtering record to update by using Sr_No")
            todo = Todo.query.filter_by(Sr_No=Sr_No).first()

            logging.info("Assign all the todo's after updation")
            todo.task_desc = task_desc
            todo.priority = priority 
            todo.due_date = due_date  # Assign converted datetime object
            todo.category = category
            todo.dependencies = dependencies
            todo.estimated_time = estimated_time 
            todo.progress = progress 
            todo.completion_reward = completion_reward

            logging.info("updated todo's added successfully")
            db.session.add(todo)
            db.session.commit()
            return redirect("/")
        
        todo = Todo.query.filter_by(Sr_No=Sr_No).first()
        return render_template('update.html', todo=todo)
    except Exception as e :
        logging.info("Error Occured in Update Route")
        raise CustomException(e)

@app.route('/delete/<int:Sr_No>') 
def delete(Sr_No) :
    try : 
        logging.info("Inside Delete Route")
        logging.info("Fetching record / todo by using Sr_No")
        todo = Todo.query.filter_by(Sr_No=Sr_No).first()
        db.session.delete(todo)
        db.session.commit()

        # Redirect back to the todo list page
        return redirect("/todo-list")
    except Exception as e :
        logging.info("Error Occured During Delete operation")
        raise CustomException(e)


@app.route('/about')
def about():
    try :
        logging.info("inside about route")
    
        return render_template('about.html')
    except Exception as e :
        logging.info("Error Occured in About route")
        raise CustomException(e)

if __name__ == "__main__":
    app.run(debug=True, port=8000)

