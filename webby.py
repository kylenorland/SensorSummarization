"""
Author: Kyle Norland
Title: Photo access server
Summary: Enables access to the python code that searches for photos

"""
from flask import Flask
from flask import render_template
from flask_cors import CORS
from flask import jsonify
from flask import request
import searchNetwork as searchNet


app = Flask(__name__)
CORS(app)
@app.route('/provideName', methods=['GET', 'POST', 'OPTIONS'])

def provideName():
    if(request.form != None):
        user = "Kyle"
        pictureTitle = "Jojo Jand"
        #userInput =" "
        #userInput = request.form['foo']
        #photoRecords = [{'user':user,'pictureTitle':pictureTitle, 'userInput':userInput}]

        """
        foundImages = dict()
        foundImages[1]="FoundImages/12-164256.jpg"
        foundImages[2]="FoundImages/12-164258.jpg"
        foundImages[3]="FoundImages/12-164300.jpg"
        """
        #triggeredWifi = 2039
        """
        triggeredWifi = 2039
        currentTime = 164256                                           #Start time is 164019
        cutoffTime = 164320
        """
        triggeredWifi = int(request.form['wifiTrigger'])
        currentTime = int(request.form['currentTime'])
        cutoffTime = int(request.form['cutoffTime'])

        print(triggeredWifi)
        print(currentTime)
        print(cutoffTime)
        
        foundList = searchNet.runNetwork(triggeredWifi, currentTime, cutoffTime)
        return jsonify(foundList)
        #return jsonify(foundImages)
        #return jsonify(user=user,
                       #pictureTitle=pictureTitle)

if __name__=='__main__':
    app.run(debug=True)
        


