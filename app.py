# INSERT DATA USING FLASK_SQLALCHEMY

from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:suman@localhost/priya'
app.config[' SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'i_love_pizza'

db = SQLAlchemy(app)

class APIUserModel(db.Model):
    __tablename__ = "bangalore"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))


@app.route('/', methods = ['GET','POST'])
def index():
# INSERT DATA
    if request.method == 'POST':
        form = request.form
        name = form['name']
        email = form['email']
        api_user_model = APIUserModel(name = name, email = email)
        save_to_database = db.session
        try:
            save_to_database.add(api_user_model) 
            save_to_database.commit()
            return redirect(url_for('write'))
        except:
            save_to_database.rollback()
            save_to_database.flush()

# READ DATA
    data = APIUserModel.query.all()   
    return render_template('write.html', data = data)

# DELETE DATA BY ID
@app.route('/delete/<int:id>')
def delete(id):
    save_to_database = db.session
    APIUserModel.query.filter_by(id = id).delete() 
    save_to_database.commit()
    return redirect(url_for('index'))

# EDIT THE DATA 
@app.route('/edit/<int:id>', methods = ['GET','POST'])
def edit(id):
    # EDIT AND SAVE NEW VALUES IN THE DATABASE
    if request.method == 'POST':
        form = request.form
        name = form['name']
        email = form['email']
        save_to_database = db.session
        try:
            api_user_model = APIUserModel.filter_by(id = id).first()
            id =  api_user_model.id
            api_user_model.name = name
            api_user_model.email = email
            save_to_database.commit()
            return redirect(url_for('index'))
        except:
            save_to_database.rollback()
            save_to_database.flush()

   # FETCH ALL DATA FOR THAT SPECIFIC ID    
    column_data = APIUserModel.query.filter_by(id = id).first()    
    return render_template('edit.html', data = column_data)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8080)