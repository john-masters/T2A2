# T2A2

## R1 - Identification of the problem you are trying to solve by building this particular app

What is the app? What problem does it solve?

The app is a simple API Web Server that controls the communication between customers and the restaurant owner. It will allow customers to view the menu and make orders for pickup (pay on pickup). For the restaurant owner, the app will allow them to see orders, update the menu, and view their total orders.

This application will remove the need for a staff member to take phone calls to take orders. It can also act as a replacement for a POS system, by keeping track of the orders, making payment when picking up the orders easy. Lastly, the app will allow the restaurant owner to keep track of past orders for their financial requirements.

---

## R2 - Why is it a problem that needs solving?

Justification for why this app is needed. Why does this problem need solving? Why do we need an app for it?

This application will significantly reduce the operating costs of the restaurant by reducing the amount of staff required. It will also save the restaurant owner money as they will have their own system that will keep track of finances, without the need for further third-party software (Applications like MYOB), or hardware (POS systems).

---

## R3 - Why have you chosen this database system. What are the drawbacks compared to others?

The database system I will be using is PostgreSQL which is a commonly used Database Management System (DBMS), belonging to the Relational Database Management System (RDBMS) variety.

Alike other DBMS such as MySQL, Microsoft SQL Server, and Oracle, they all share a similar syntax as they are all based on SQL which allows developers to easily use these different programs.

Postgres is also open source software, which means that it can be used for free, for whatever business or personal needs you may require. In addition, it's available on Windows, Mac and Linux so it's easily available regardless of your operating system.

Fortunately, there are few disadvantages to PostgreSQL although there a few. One of these is PostgreSQL is slower than MySQL, although for most use cases this won't be too noticable unless you're dealing with very large databases.

Another disadvantage is that PostgreSQL is less supported than MySQL. None of these disadvantages are detrimental to using PostgreSQL, and it is still a great choice as a DBMS for a huge variety of needs.

PostgreSQL: A closer look at the object-relational database management system (2022) IONOS Digital Guide. IONOS. Available at: <https://www.ionos.com/digitalguide/server/know-how/postgresql/> (Accessed: October 23, 2022).

Peterson, R. (2022) What is PostgreSQL? Introduction, Advantages & Disadvantages, Guru99. Available at: <https://www.guru99.com/introduction-postgresql.html> (Accessed: October 23, 2022).

---

## R4 - Identify and discuss the key functionalities and benefits of an ORM

The key functionalities of an ORM, which in our case is SQLAlchemy, are to have a library of functionalities which allow the developer to interact with the database through the application. Not only does this allow you to develop user-friendly methods for accessing the database, but it also allows you to improve the security of the database with data sanitising practices. Other benefits are that it makes you write code with MVC architecture, which keeps the code clean and overall more DRY.

[source](https://stackoverflow.com/questions/1279613/what-is-an-orm-how-does-it-work-and-how-should-i-use-one)

---

## R5 - Document all endpoints for your API

### Signup

- HTTP request verb: POST
- Required data where applicable: Name, email address and password
- Expected response data: UserSchema
- Authentication methods where applicable: n/a

### Signin

- HTTP request verb: POST
- Required data where applicable: The email address and password in JSON format
- Expected response data: JWT Token in JSON format
- Authentication methods where applicable: username and hashed password is checked against db

### User list

- HTTP request verb: GET
- Required data where applicable: n/a
- Expected response data: List of UserSchemas
- Authentication methods where applicable: JWT Token and admin role

### Delete users

- HTTP request verb: DELETE
- Required data where applicable: user id
- Expected response data: Message confirming user has been deleted
- Authentication methods where applicable: JWT Token and admin role

### Get menu

- HTTP request verb: GET
- Required data where applicable: n/a
- Expected response data: List of all food items on menu
- Authentication methods where applicable: n/a

### Update food items

- HTTP request verb: PUT or PATCH
- Required data where applicable: Food item id in URL, and data to be updated in JSON format
- Expected response data: Confirmation message and updated food schema
- Authentication methods where applicable: Admin JWT Token and admin role

### Add food items

- HTTP request verb: POST
- Required data where applicable: Food name, price, ingredients and is_veg in JSON format
- Expected response data: Confirmation message and new food schema
- Authentication methods where applicable: Admin JWT Token and admin role

### Post orders

- HTTP request verb: POST
- Required data where applicable: All of the food ids for each item
- Expected response data: Order confirmation and order id
- Authentication methods where applicable: JWT Token

### Get orders

- HTTP request verb: GET
- Required data where applicable: n/a
- Expected response data: If user is admin, list of all order schemas. If user is customer, list of their order schemas
- Authentication methods where applicable: JWT Token

### Get current orders

- HTTP request verb: GET
- Required data where applicable: n/a
- Expected response data: If user is admin, list of all order schemas except orders with the status of 'Completed' or 'Refunded'. If user is customer, list of their order schemas except orders with the status of 'Completed' or 'Refunded'
- Authentication methods where applicable: JWT Token

### Get past orders

- HTTP request verb: GET
- Required data where applicable: n/a
- Expected response data: If user is admin, list of all order schemas with the status of 'Completed' or 'Refunded'. If user is customer, list of their order schemas with the status of 'Completed' or 'Refunded'
- Authentication methods where applicable: JWT Token

### Create orders

- HTTP request verb: POST
- Required data where applicable: Food id and quantity for first item
- Expected response data: Confirmation message and order schema (Email is sent to customer with order details as well)
- Authentication methods where applicable: JWT Token

### Add items to order

- HTTP request verb: PUT or PATCH
- Required data where applicable: Order id in URL, food id and quantity in JSON format
- Expected response data: Confirmation message and updated order schema (Email is sent to customer with order details as well)
- Authentication methods where applicable: JWT Token

### Update order status

- HTTP request verb: PUT or PATCH
- Required data where applicable: Associated order ID in URL and desired order status in JSON format
- Expected response data: Updated order schema (Email is sent to customer with updated order details as well)
- Authentication methods where applicable: Admin JWT Token and admin role

### Delete orders for restaurant owner

- HTTP request verb: DELETE
- Required data where applicable: Associated order ID in URL
- Expected response data: Confirmation message the order is deleted
- Authentication methods where applicable: Admin JWT Token and admin role

### Delete order items for customer

- HTTP request verb: DELETE
- Required data where applicable: Associated order ID followed by the order item ID in URL
- Expected response data: Confirmation message the order item is deleted
- Authentication methods where applicable: JWT Token and customer role (only the customer who placed the order can delete items from it)

---

## R6 - An ERD for your app

![ERD](docs/ERD.jpg)

---

## R7 - Detail any third party services that your app will use

When customers make orders, they will receive an order confirmation email via the SendGrid API. The email will contain the order details, including the order id, the items ordered, the quantity of each item, the subtotal for each item, the total price and the order status.

When customers update their orders, they will receive an order confirmation email via the SendGrid API. The email will contain the updated order details, including the order id, the items ordered, the quantity of each item, the subtotal for each item, the total price and the order status.

When admins update the status of an order, the customer will receive an order confirmation email via the SendGrid API. The email will contain the updated order details, including the order id, the items ordered, the quantity of each item, the subtotal for each item, the total price and the new order status.

---

## R8 - Describe your projects models in terms of the relationships they have with each other

### Users

- The user model has id, name, email, password, is_admin and orders columns.
- The orders column is a relationship with the orders table, which, when queried, will return all of the orders associated with that user.

### Orders

- The order model has id, user_id, status, total_price and order_items columns.
- The user_id column is a foreign key that references the id column in the users table.
- The order_items column is a relationship with the order_items table, which, when queried, will return all of the order items associated with that order.

### Order Items

- The order item model has id, order_id, food_id, quantity and subtotal columns.
- The order_id column is a foreign key that references the id column in the orders table.
- The food_id column is a foreign key that references the id column in the food table.

### Food

- The food model has id, name, price, ingredients, is_veg and on_menu columns.

---

## R9 - Discuss the database relations to be implemented in your application

The first relationship is the User model which has a one-to-many relationship with the Order model. This means that a user can have many orders, but an order can only have one user. The order model has a user_id foreign key which links it to the user model.

The second relationship is the Order model which has a one-to-many relationship with the OrderItem model. This means that an order can have many order items, but an order item can only have one order. The order item model has an order_id foreign key which links it to the order model.

The third relationship is the Food model which has a one-to-many relationship with the OrderItem model. This means that a food can be associated with many order items, but an order item can only have one food. The order item model has a food_id foreign key which links it to the food model.

---

## R10 - Describe the way tasks are allocated and tracked in your project

To facilitate the tracking of tasks, I used Trello to create a Kanban board with columns for To Do, Doing and Done. In the beginning, I created a list of tasks that needed to be completed, and then I moved them to the To Do column.

The tasks were ordered in the To Do column by priority. The tasks that needed to be completed first were at the top of the list, and the tasks that could be completed later were at the bottom of the list.

As I started working on a task, I moved it to the Doing column. Once I completed a task, I moved it to the Done column. This allowed me to keep track of what I had completed and what I still needed to do.

See the Kanban board [here](https://trello.com/invite/b/LsTz9le2/ATTIcb57bcfce81384249b7ec8371ced357b990C3768/t2a2-kanban).

---

### Postgresql instructions to set up database

- Create database

```sql
CREATE DATABASE pizzeria;
```

- Create user

```sql
CREATE USER pizza WITH PASSWORD 'cheese';
```

- Grant privileges

```sql
GRANT ALL PRIVILEGES ON DATABASE pizzeria TO pizza;
```
