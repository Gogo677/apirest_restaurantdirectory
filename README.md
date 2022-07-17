# RESTFULL-API directorio de restaurantes
Se crea una resfull-API para listar restaurantes.

## Esta versión usa ejemplo de conexión a SQL server
La actual versión solo contiene los métodos: 
## /restaurants
* GET para obtener el listado de restaurantes
* POST para insertar un restaurante (requiere credenciales de usuario registrado)
## /restaurants/id
* PUT para editar la información de un restaurante (requiere credenciales de usuario registrado)
* DELETE para eliminar la información de un restaurante (requiere credenciales de usuario registrado)
## /users
* POST para registrar nuevos usuarios
## /auth
* POST para autentificar usuarios existentes

Fue implementado para usarse con una base de datos SQLserver en Python usando Flask, SQLalchemy y marshmallow.