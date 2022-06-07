'''
This Project is Made by Team-Ignite for Smart India Hackathon (SIH).

Topic : Digital Access Code generation and use for address tracking - AK1207 - 425 (Software).

MIT License

Copyright (c) 2022 TEAM IGNITE

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''


# Imports for WebApp
from flask import *

# Importing geopy library (For Coordinates)
from geopy.geocoders import Nominatim

# Imports for PlusCodeApi
import requests
import json


# Global Variables
GENERATED = False
VERIFIED = False




app = Flask(__name__,template_folder='template',static_folder='static')


# Function which takes Address and Gives Coordinates

def findcoordinates(address):

    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(address)
    # print(getLoc.address)
    # print("Latitude = ", getLoc.latitude, "\n")
    # print("Longitude = ", getLoc.longitude)

    return getLoc.address,getLoc.latitude,getLoc.longitude

# Function to find plus code using Coordinates

def findpluscode(lat,long):
    s1 = str(lat) + ',' +str(long)
    parameters = {
        # 'address' : '19.108914019118583, 72.86535472954193'
        'address' : str(s1)
    }
    response = requests.get("https://plus.codes/api", params=parameters)
    r = json.loads(response.text)
    return r['plus_code']['global_code']


# Function to find Address using Coordinates

def findaddressusingcoordinates(lat,long):
    s1 = str(lat) + ',' + str(long)
    geoLoc = Nominatim(user_agent="GetLoc")
    locname = geoLoc.reverse(s1)
    return str(locname.address)






@app.route("/")
def LandingPage():
    return render_template('LandingPage.html')


@app.route("/main")
def Main():
    return render_template('MainPage.html', generated = GENERATED)


@app.route("/about")
def AboutPage():
    return render_template('About.html')


@app.route("/generate", methods=['GET', 'POST'])
def GenerateCode():
    global GENERATED

    if request.method == "POST":
        GENERATED = True
        flat_building = str(request.form['flat_building'])
        street = str(request.form['street'])
        city = str(request.form['city'])
        state = str(request.form['state'])
        country = str(request.form['country'])
        pincode = str(request.form['pincode'])

        # print(flat_building)
        # print(street)
        # print(city)
        # print(state)
        # print(country)
        # print(pincode)

        # This Address dosent contain flat and Building
        address = str(street + ',' + city + ',' + country + ',' + pincode)
        print(address)

        a,b,c = findcoordinates(address)
        print(a,b,c)

        pluscode = findpluscode(float(b),float(c))

        return render_template('GenerateCode.html', generated = GENERATED, global_address = a, latitude_generated = b, longitude_generated = c, plus_code = pluscode)

        


    GENERATED = False
    return render_template('GenerateCode.html', generated = GENERATED)


@app.route("/verify", methods=['GET', 'POST'])
def Verify():
    global VERIFIED

    if request.method == "POST":
        VERIFIED = True
        latitude = str(request.form['lat'])
        longitude = str(request.form['long'])
        # IDAC = str(request.form['IDAC'])
        globaladdress = findaddressusingcoordinates(latitude,longitude)
        pluscode = findpluscode(latitude,longitude)
        return render_template('VerifyCode.html', verified=VERIFIED, global_address=globaladdress, plus_code=pluscode, latitude_generated=latitude,longitude_generated=longitude)
        

        


    VERIFIED = False
    return render_template('VerifyCode.html', verified=VERIFIED)







if __name__ == "__main__":
    app.run(debug=True)