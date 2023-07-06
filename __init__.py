from flask import Flask,request,jsonify,abort
import pymongo

#app
app = Flask(__name__)

#database
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

#API
@app.route('/request', methods=['POST'])
def postRequest():
    mydict = { "name": request.json['name'], "address": request.json['address']}
    mydb.customers.insert_one(mydict)
    return 'post finish'

@app.route('/request', methods=['GET'])
def getRequest():
    data = []
    for x in mydb.customers.find({},{ "_id": 1, "name": 1, "address": 1 }):
        x['_id'] = str(x['_id'])
        data.append(x)
    print(data)
    return  jsonify({'data':data})

@app.route('/request', methods=['PUT'])
def putRequest():
    data = request.json
    name = data.get('name')
    new_name = data.get('new_name')
    new_address = data.get('new_address')

    doc = mydb.customers.find_one({"name": name})#find data
    if new_name:
        myquery = { "name": doc["name"] }
        newvalues = { "$set": { "name": new_name }}
        mydb.customers.update_one(myquery, newvalues)
        print("in name")
    if new_address:
        myquery = { "address": doc['address'] }
        newvalues = { "$set": { "address": new_address } }
        mydb.customers.update_one(myquery, newvalues)
        print("in address")

    

    print(new_name)
    print(new_address)
    return 'put finish'

@app.route('/request/<name>', methods=['DELETE'])
def deleteRequest(name):
    myquery = { "name": name}
    mydb.customers.delete_one(myquery)
    return 'delete finish'