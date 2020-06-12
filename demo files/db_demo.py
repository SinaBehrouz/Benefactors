from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
#The URL may be a db_Server i.e. postgress or on file db (i.e. sqlite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#first I would like to go over some configuration tokens which I found very useful in web-development
#some of these are also available in sqlalchemy but its not as intuitive to configure.

#some new features of SQLAlchemy:
#SQLALCHEMY_POOL_SIZE allow you to specify the size of db pool.
#the default value is dependent on the engine you're using
#app.config['SQLALCHEMY_POOL_SIZE'] = 10

#Certain database backends may impose different inactive connection timeouts,
#which interferes with Flask-SQLAlchemy’s connection pooling.
#if you're using a backend db with low connection time out, its a good idea to set the
#recycle token to a value less than the time out connection to keep the connection alive.
#SQLALCHEMY_POOL_RECYCLE is Number of seconds after which a connection is automatically recycled
#for example in MySQL the connection is removed after 8hr of being idle, in this case we are
#reseting the connection after every 5 hrs - by default this value is 2 hrs.
#app.config['SQLALCHEMY_POOL_RECYCLE'] = 18000

#Specifies the connection timeout in seconds for the pool
#app.config['SQLALCHEMY_POOL_TIMEOUT'] = 19000

# In almost all web-dev applications you're bound to use multiple databases, and
# binding can be very helpful in these scenarios.
# SQLALCHEMY_DATABASE_URI token will allow for a default db, but here we are also creating connections
# to 2 other databases.
# in order to interact with these database they must be addressed and in this demo I will show
# as we go along how it can be acheieved.
#app.config['SQLALCHEMY_BINDS']={
#    'users':        'mysqldb://localhost/users',
#    'appmeta':      'sqlite:////path/to/appmeta.db'
#}

db = SQLAlchemy(app)


class Students(db.Model):
    ##If you declare a model you can specify the bind to use with the __bind_key__ attribute
    #If you specified the __bind_key__ on your models you can use them exactly the way you are used to.
    #The model connects to the specified database connection itself.
    #__bind_key__ = 'users'
    studentId = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    major = db.Column(db.String(50))
    gpa = db.Column(db.Float, default = 0.00)
    #this class will be modeled to a table eventually
    #ORM
    #id is generate automatically upon instantiating an object
    classes = db.relationship('Courses', backref = 'students', lazy = True)
    def __repr__(self):
        return f"User('{self.studentId}','{self.firstName}','{self.gpa}')"

class Courses(db.Model):
    cid = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), unique= True, nullable = False)
    units = db.Column(db.Integer, nullable = False)
    sid = db.Column(db.Integer, db.ForeignKey('students.studentId'), nullable = False)

    def __repr__(self):
        return ""
        #return f"User('{self.Dean}','{self.title}','{self.sid}')"


@app.route('/<int:student_id>', methods=['GET'])
def student_info(student_id):
    student = Students.query.filter_by(studentId = student_id).all()
    print(student)
    print(type(student))
    print(student[0].studentId)
    return render_template('db.html', student = student[0])

def CreateTable(db):
    #creating table
    db.create_all()


def populate_db(db):
    sitems = []
    sitems.append( Students(firstName = "Mark", lastName ="Smith",major = "Engineering", gpa = "3.00") )
    sitems.append( Students(studentId = 214, firstName = "Josh", lastName ="Hudson",major = "Arts", gpa = "3.30") )
    sitems.append( Students(studentId = 301, firstName = "Zac", lastName ="Efron",major = "Comp-Sci", gpa = "4.00") )
    sitems.append( Students(studentId = 431,firstName = "Leonardo", lastName ="DiCaprio",major = "Engineering", gpa = "4.00") )
    sitems.append( Students(studentId = 723,firstName = "Tom", lastName ="Hanks",major = "Sciences", gpa = "1.00") )
    sitems.append( Students(firstName = "George", lastName ="Clooney",major = "Crim", gpa = "4.00") )
    for el in sitems:
        db.session.add(el)
    db.session.commit()

    citems = []
    citems.append( Courses(title="CMPT-470", units = 3, sid = 1) )
    citems.append( Courses(title="CMPT-310", units = 3, sid = 214) )
    citems.append( Courses(title="CMPT-354", units = 3, sid = 301) )
    citems.append( Courses(title="ENSC-327", units = 4, sid = 431) )
    citems.append( Courses(title="Arts-100", units = 2, sid = 723) )
    citems.append( Courses(title="Crim-201", units = 3, sid = 724) )

    for el in citems:
        db.session.add(el)
    db.session.commit()
    print("db populated")
