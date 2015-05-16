from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


### General Write to DB
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()
session.query(Restaurant).all()

### General Write to DB
cheesepizza = MenuItem(name = "Cheese Pizza", description = "made with all natural ingredients and fresh mozzarella", course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()
session.query(MenuItem).all()

#General Reading
firstResult = session.query(Restaurant).first()
firstResult.name

#Updating DB:
Veggie = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for x in Veggie:
	print x.id
	print x.price
	print x.restaurant.name
	print "/n"
	
### Updating = 3 steps:
#1. Find Entry store in variable (update value)
#2. session.add(variable)
#3. session.commit()

#$7.50
#Urban Burger

#10
#$5.99
#Urban Burger

UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 2).one()
print UrbanVeggieBurger.price
#$7.50
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()
#2
#$2.99
#Urban Burger

### Deleting = 3 steps:
#1. Find entry...spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
#2. session.delete(entry)
#3. session.commit()

