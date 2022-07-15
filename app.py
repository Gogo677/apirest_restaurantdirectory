from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
# Configuracion de motor de base de datos

#------Configuracion para Microsoft SQL server-----------
#app.config['SQLALCHEMY_DATABASE_URI'] ='mssql+pymssql://username:password@hostname:port/dbname'

#Configuracion para MYSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/apiprueba'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# !!!!----- Nota: la base de datos ya debe estar creada, las tablas las generara despues si no existen------!!!!

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Creacion de tablas con db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), unique=True)
    email = db.Column(db.String(70),unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, email,password):
        self.username = username
        self.email = email
        self.password = password

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurantName = db.Column(db.String(70))
    restaurantType = db.Column(db.String(30))
    address= db.Column(db.String(70))
    phone= db.Column(db.String(70))

    def __init__(self, restaurantName, restaurantType,address,phone):
        self.restaurantName = restaurantName
        self.restaurantType = restaurantType
        self.address = address
        self.phone = phone
# Método que crea las tablas
db.create_all()

# Crea un schema para interactuar con los datos 
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email','password')

class RestaurantSchema(ma.Schema):
    class Meta:
        fields = ('id', 'restaurantName', 'restaurantType','address','phone')


user_schema = UserSchema()
#users_schema = UserSchema(many=True)

restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)

#Creación de restaurantes de prueba en la db
def insertRestaurants():
    restaurants = [
    {'restaurantName':'Pizza Charly', 'restaurantType': 'pizza','address': 'Manzana123','phone':'111-111-111'},
    {'restaurantName':'Tacos Pedro', 'restaurantType': 'tacos','address': 'Apple321','phone':'222-222-222'},
    {'restaurantName':'Burger Kindom', 'restaurantType': 'fast-food','address': 'Pearl987','phone':'333-333-333'}]

    for restaurant in restaurants:
        new_restaurant=Restaurant(restaurant['restaurantName'], restaurant['restaurantType'],restaurant['address'],restaurant['phone'])

        db.session.add(new_restaurant)

    db.session.commit()    



# Endpoints

# Obtener lista de restaurantes
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    #insertRestaurants() #Esta linea inserta restaurantes
    all_restaurants = Restaurant.query.all()
    result = restaurants_schema.dump(all_restaurants)
    return jsonify(result)

# insertar restaurante
@app.route('/restaurants', methods=['POST'])
def create_task():
  restaurantName = request.json['restaurantName']
  restaurantType = request.json['restaurantType']
  address = request.json['address']
  phone = request.json['phone']

  new_restaurant = Restaurant(restaurantName, restaurantType,address,phone)

  db.session.add(new_restaurant)
  db.session.commit()
  #restaurant_schema.jsonify(new_restaurant)

  return jsonify({'Message':'Restaurant added successfully', 'Values': request.json}) 


# Crear usuario
@app.route('/users',methods=['POST'])
def create_user():
    username= request.json['username']
    email=request.json['email']
    password=request.json['password']

    new_user = User(username, email, password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"Message":'User added successfully'})

# Autentificar usuario
@app.route('/auth',methods=['POST'])
def auth_user():
    username = request.json['username']
    password = request.json['password']
    print(username,password)

    us=User.query.filter_by(username=username,password=password).first()

    print(us)
    if us is not None:
        return jsonify({"Message":'User exist'})
    else:
        return jsonify({"Message":'Failed authenticade user'})    

if __name__ == "__main__":
    app.run(debug=True,port=4000)
