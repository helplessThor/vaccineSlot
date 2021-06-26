from flask import *
import json, requests
from datetime import date


class VaccineSlots:
    def __init__(self, name, address, pincode, vaccine_name, age_group, dose1, dose2, fee):
        self.name = name
        self.address = address
        self.pincode = pincode
        self.vaccine_name = vaccine_name
        self.age_group = age_group
        self.dose1, self.dose2 = dose1, dose2
        self.fee = fee


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return "WE ENCOUNTERED SOME PROBLEM, PLEASE TRY AGAIN LATER OR CONTACT teamgocorona@gmail.com"


@app.errorhandler(413)
def page_not_found(e):
    return "YOU HAVE ENTERED FILE BEYOND CAPACITY LIMIT, CHECK INSTRUCTIONS AND TRY AGAIN."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=['GET','POST'])
def check():
    if request.method == 'POST':

        print("HERe")
        district = request.form.get("dis_id")
        today = date.today().strftime("%d-%m-%Y")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        api_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id="+district+"&date=" + today

        response = requests.get(api_url, headers)
        res = response.json()
        final = res['sessions']

        av_list = []
        for i in range(len(final)):
            if final[i]['available_capacity_dose1'] > 0 or final[i]['available_capacity_dose2'] > 0:
                av_list.append(VaccineSlots(final[i]['name'], final[i]['address'], final[i]['pincode'],
                                            final[i]['vaccine'], final[i]['min_age_limit'],
                                            final[i]['available_capacity_dose1'],
                                            final[i]['available_capacity_dose2'], final[i]['fee']))

        av_list.sort(key=lambda x: x.name)
        # for obj in av_list:
        #     print(obj.name, obj.address + ", " + str(obj.pincode), obj.vaccine_name, obj.age_group, obj.dose1,
        #           obj.dose2, obj.fee)
        return render_template("index.html", list=av_list)
    return render_template("index.html")


app.run(debug=True)
