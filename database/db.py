import mysql.connector
import unicodedata
import re 
import json 

mydb = mysql.connector.connect(
  host="localhost",   # Host 
  user="root",        # User 
  passwd="password",  # Password 
  db= "mydatabase"    # Name of the database 
)

def getUsers(db = mydb, status = None, year = None ):
  '''
      Method that retrieves all the information from User and Contract database.

      returns @dictionary with {userId : userInformation} 
  '''

  mycursor = db.cursor()

  if year:
    year = int(ustr(year)) # Conversion from unicode to in 

  # Retrieve basic data from every user
  # Cells containing all the information to be filled 
  cells = [
    'name','personalID','companyID',
    'GYM price', 'FOOD price', 'RENTING price','FORMATION price',
    'TRANSPORT price','KINDERGARTEN price', 'LIFE-INSURANCE price', 'LIFE-INSURANCE start date',
    'HEALTH-INSURANCE price', 'HEALTH-INSURANCE start date','LOTTERY price', 'LOTTERY ticket'
    ]

  data_cells = [ '-' for i in range(15)] # - by default

  mycursor.execute("SELECT id, firstName, lastName1, lastName2, personalID, companyID FROM User")
  myusers = mycursor.fetchall()
  
  users_dict = dict() # Dictionary with id containing all information above for each user. 

  for user in myusers:
    data_cells[0] = "{} {} {}".format(ustr(user[1]),ustr(user[2]),ustr(user[3])) # Name 
    data_cells[1] = ustr(user[4]) # personalID
    data_cells[2] = user[5] # companyID
    users_dict[user[0]] =  dict(zip(cells,data_cells)) 
  
  
  # Retrieve data from every specific user
  mycursor.execute("SELECT userId, product, price,  details, status, year FROM Contract")
  myuser_data = mycursor.fetchall() 
  
  for data in myuser_data:
    userId = data[0] # User Id 
    if ((status != None and data[4] == status) or status == None) and ((year != None and year == data[5]) or year == None):
      product = ustr(data[1]) # Product name 
      data_fill = get_inf_to_fill(product) # Data to be filled in the dictionary
      
      if data_fill != None:
        users_dict[userId][data_fill[0]] = data[2] # Update price 
        
        if len(data_fill) == 2:
          details = json.loads(data[3]) # Encode details as JSON object
          
          if details.has_key('0'):
             
             if details['0'].has_key(data_fill[1][1]): # Check's if this is a family JSON and gets User '0'
              users_dict[userId][data_fill[1][0]] = details['0'][data_fill[1][1]] # Updates User details
          
          if details.has_key(data_fill[1][1]):
            users_dict[userId][data_fill[1][0]] = details[data_fill[1][1]] # Updates User Details
  
  return users_dict

def dict_to_list(users_dict):
  '''
    Method that returs a list of list based on the dictionary passed as parameter
    Used to structure the .csv file
  '''
  data_order = [
    'name' ,'personalID' ,'companyID', 
    'GYM price', 'FOOD price', 'RENTING price','FORMATION price',
    'TRANSPORT price','KINDERGARTEN price', 'LIFE-INSURANCE price', 'LIFE-INSURANCE start date',
    'HEALTH-INSURANCE price', 'HEALTH-INSURANCE start date','LOTTERY price', 'LOTTERY ticket'
  ]
  users_list =  [['id'] + [field_name for field_name in data_order]]

  for id in users_dict:

    user_ix = [id] + [ users_dict[id][data] for data in data_order]
    users_list.append(user_ix)

  return users_list



# Support method
def get_inf_to_fill(product):
  '''
    Method that returns a list  with the information to be filled in the dictionary 
  '''
  only_price = ['gym','food','renting','formation','transport','kindergarten']
  date_price = ['life-insurance','health-insurance']

  if product in only_price:
    return ['{} price'.format(product.upper())]
  elif product.lower() in date_price:
    prod = product.upper()
    return ['{} price'.format(prod) , ['{} start date'.format(prod),'startDate']]
  elif product == 'lottery':
    prod = product.upper()
    return ['{} price'.format(prod), ['{} ticket'.format(prod),'ticketCount']]
  return None 


#Support Method
def ustr(string):
  '''
    Encode strings from Unicode to ASCII
  '''
  if string is None:
    return ''
  return string.encode('ascii','ignore')