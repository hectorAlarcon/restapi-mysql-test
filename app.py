from flask import Flask, jsonify, request 
import flask_excel as excel
app = Flask(__name__)

from database.db import mydb, getUsers, dict_to_list


@app.route("/show")
def show():
    '''
        Method that shows the information. 
    '''
    
    filename = 'user_data'

    status = request.args.get('status') # Query param for status
    year = request.args.get('year')     # Query param for year 
    
    if year :
        filename = filename + '_y-'+ year
    if status:
        filename = filename + '_stat-'+ status
    data = getUsers(status=status, year=year)

    return jsonify({"title": filename, "message":data})


@app.route("/download", methods=['GET'])
def download_file():
    '''
        Method that downloads a .csv containing al the information.

        query params :
            status = Only extracts information that meet the status requirement
            year   = Only extracts informations from the exact year passed.
    '''
    
    filename = 'user_data'

    status = request.args.get('status') # Query param for status
    year = request.args.get('year')     # Query param for year 
    
    if year :
        filename = filename + '_y-'+ year
    if status:
        filename = filename + '_stat-'+ status

    data = getUsers(status=status, year=year)
    data = dict_to_list(data)

    return excel.make_response_from_array(data, "csv",file_name= filename)

if __name__ == "__main__":
    excel.init_excel(app)
    app.run(debug = True, port = 5000)