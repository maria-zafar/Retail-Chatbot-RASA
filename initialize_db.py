import sqlite3
conn = sqlite3.connect('example.db')

c = conn.cursor()

# Create table
# c.execute('''CREATE TABLE orders
#              (text, trans text, symbol text, qty real, price real)''')


# Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# EXISTING ORDERS
# Create table
c.execute('''CREATE TABLE orders
             (order_date, order_number, order_email, color, size, status)''')

# data to be added
purchases = [('2006-01-05',123456,'example@rasa.com','blue', 9, 'shipped'),
             ('2021-01-05',123457,'me@rasa.com','black', 10, 'order pending'),
             ('2021-01-05',123458,'me@gmail.com','gray', 11, 'delivered'),
            ]

# add data
c.executemany('INSERT INTO orders VALUES (?,?,?,?,?,?)', purchases)

# # AVAILABLE INVENTORY
# # Create table
# c.execute('''CREATE TABLE inventory
#              (size, color)''')

# # data to be added
# inventory = [(7, 'blue'),
#              (8, 'blue'),
#              (9, 'blue'),
#              (10, 'blue'),
#              (11, 'blue'),
#              (12, 'blue'),
#              (7, 'black'),
#              (8, 'black'),
#              (9, 'black'),
#              (10, 'black')
#             ]

# # add data
# c.executemany('INSERT INTO inventory VALUES (?,?)', inventory)

# AVAILABLE INVENTORY
# Create table
c.execute('''CREATE TABLE inventory
              (size, color, gender, product_category, style)''')

# data to be added
inventory = [(7, 'blue', 'female', 'shoe', 'boots'),
             (7, 'blue', 'female', 'shoe', 'boots'),
              (8, 'blue', 'female', 'shoe', 'pumps'),
              (9, 'blue','female', 'shoe', 'high heels'),
              (10, 'blue', 'male', 'shoe', 'boots'),
              (11, 'blue','male', 'shoe', 'joggers'),
              (12, 'blue','female', 'shoe', 'boots'),
              (7, 'black','female', 'shoe', 'high heels'),
              (8, 'black','female', 'shoe', 'pumps'),
              (9, 'black','female', 'shoe', 'boots'),
              (10, 'black','male', 'shoe', 'boots'),
              (7, 'green', 'female', 'shoe', 'boots'),
              (8, 'white', 'female', 'shoe', 'pumps'),
              (9, 'red','female', 'shoe', 'high heels'),
              (10, 'brown', 'male', 'shoe', 'boots'),
              (11, 'black','male', 'shoe', 'joggers'),
              (12, 'red','female', 'shoe', 'boots'),
              (7, 'red','female', 'shoe', 'high heels'),
              (8, 'black','male', 'shoe', 'dress shoes'),
              (9, 'black','male', 'shoe', 'sneakers'),
              (10, 'black','male', 'shoe', 'loafers'),
              (7, 'white', 'female', 'shoe', 'sandals'),
              (8, 'brown', 'female', 'shoe', 'sandals'),
              (9, 'brown','female', 'shoe', 'high heels'),
              (10, 'blue', 'male', 'shoe', 'sandals'),
              (11, 'black','male', 'shoe', 'sandals'),
              (12, 'brown','male', 'shoe', 'sandals'),
              (7, 'black','female', 'shoe', 'wedges'),
              (8, 'black','female', 'shoe', 'wedges'),
              (9, 'black','female', 'shoe', 'flats'),
              (10, 'black','male', 'shoe', 'sandals')
            ]

# add data
c.executemany('INSERT INTO inventory VALUES (?,?,?,?,?)', inventory)


# Save (commit) the changes
conn.commit()

# end connection
conn.close()