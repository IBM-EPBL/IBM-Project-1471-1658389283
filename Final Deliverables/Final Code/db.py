from pymongo import MongoClient, cursor

CONNECTION_STRING = "mongodb://127.0.0.1:27017/"    
client = MongoClient(CONNECTION_STRING)   
mydb = client['user']
information = mydb.userinformation




def check_ifavailable(email):
   query={'email':email}
   a = information.find(query)   
   l=0
   for i in a:
      print(i)
      l=l+1 
   
   if(l==0):      
      return 1
   else:
      return 0
   



def insert_database(name,email,password):   

   records = {
      'name':name,
      'email':email,
      'password':password     
   }   
   information.insert_one(records)

def check_for_password(email):
   query={'email':email}
   a = information.find(query)  
   t = ""
   for i in a:
      t = i['password']
   
   if(t==""):      
      return 0 
   else:
      return t

def get_userame(email):
   query={'email':email}
   a = information.find(query)  
   t = ""
   for i in a:
      t = i['name']    
   return t
   
   


      

   
  
