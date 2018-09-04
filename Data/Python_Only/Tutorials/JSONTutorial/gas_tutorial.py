import json
from pprint import pprint
import sqlite3
from datetime import datetime
# http://www.prelc.si/koleznik/tutorial-for-parsing-json-and-creating-sqlite3-database-in-python/

DATE_FORMAT = '%Y-%m-%d'

database = "Data/Python_Only/Tutorials/JSONTutorial/GasPrices.db"
rawfile = 'Data/Python_Only/Tutorials/JSONTutorial/gas_tutorial_data.json'


class GasPrices():
    def __init__(self, json_dict, type_of_gas, normal=True):
        self.normal_higher = "normal" if normal else "higher"

        # Here we're setting the type of gas which is one of the objects in the JSON, analogous to the bookid from the librarything data. I want to set this field as the userid?
        self.type_of_gas = type_of_gas

        # This line looks like it's indicating that the data that goes into the tax_co2 field should be the data located at the indicated type_of_gas.normal.tax_co2
        self.tax_co2 = json_dict[type_of_gas][self.normal_higher]["tax_co2"]
        self.tax = json_dict[type_of_gas][self.normal_higher]["tax"]
        self.charge = json_dict[type_of_gas][self.normal_higher]["charge"]
        self.updated = json_dict[type_of_gas][self.normal_higher]["updated"]
        self.excise_duty = json_dict[type_of_gas][self.normal_higher]["excise_duty"]
        self.price = json_dict[type_of_gas][self.normal_higher]["price"]
        self.price_neto = json_dict[type_of_gas][self.normal_higher]["price_neto"]


class Country():
    def __init__(self, country, json_dict):

        # When the function is invoked, call the Country class and pass in the name of the country as written in the JSON outermost object.
        self.jsonDict = json_dict[country]
        self.country = country

        self.currency = self.jsonDict["currency"]
        self.gas_100 = GasPrices(self.jsonDict, "100")
        self.gas_95 = GasPrices(self.jsonDict, "95")
        self.diesel = GasPrices(self.jsonDict, "diesel")
        self.ko = GasPrices(self.jsonDict, "ko")

    def __repr__(self):
        print("Price for diesel: ", self.diesel.price)
        print("Price for 100: ", self.gas_100.price)
        print("Price for 95: ", self.gas_95.price)
        print("Price for fuel oil: ", self.ko.price)
        return(self.country)

    def save_to_database(self):
        con = sqlite3.connect(database)
        with con:
            cur = con.cursor()
            con.row_factory = sqlite3.Row

            # Checks if the entry is updated
            cur.execute("SELECT updated FROM GasPrice WHERE country=? AND gas_type=?",
                        (self.country, self.diesel.type_of_gas))

            should_update_diesel = False

            i = 0
            while True:
                row = cur.fetchone()
                if (row == None):
                    if (i == 0):
                        should_update_diesel = True
                    break
                if (datetime.strptime(row[0], DATE_FORMAT) < datetime.strptime(self.diesel.updated, DATE_FORMAT)):
                    should_update_diesel = True
                i += 1

            if (should_update_diesel):
                cur.execute("INSERT INTO GasPrice"
                            "("
                            "country,"
                            "currency,"
                            "gas_type,"
                            "normal,"
                            "price,"
                            "price_neto,"
                            "charge,"
                            "excise_duty,"
                            "tax,"
                            "tax_co2,"
                            "updated"
                            ") VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                            (
                                self.country,
                                self.currency,
                                self.diesel.type_of_gas,
                                1,
                                self.diesel.price,
                                self.diesel.price_neto,
                                self.diesel.charge,
                                self.diesel.excise_duty,
                                self.diesel.tax,
                                self.diesel.tax_co2,
                                self.diesel.updated
                            )
                            )
            cur.execute("SELECT updated FROM GasPrice WHERE country=? AND gas_type=?",
                        (self.country, self.gas_100.type_of_gas))

            should_update_gas_100 = False

            i = 0
            while True:
                row = cur.fetchone()
                if (row == None):
                    if (i == 0):
                        should_update_gas_100 = True
                    break
                if (datetime.strptime(row[0], DATE_FORMAT) < datetime.strptime(self.diesel.updated, DATE_FORMAT)):
                    should_update_gas_100 = True
                i += 1
            if (should_update_gas_100):
                cur.execute("INSERT INTO GasPrice"
                            "("
                            "country,"
                            "currency,"
                            "gas_type,"
                            "normal,"
                            "price,"
                            "price_neto,"
                            "charge,"
                            "excise_duty,"
                            "tax,"
                            "tax_co2,"
                            "updated"
                            ") VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                            (
                                self.country,
                                self.currency,
                                self.gas_100.type_of_gas,
                                1,
                                self.gas_100.price,
                                self.gas_100.price_neto,
                                self.gas_100.charge,
                                self.gas_100.excise_duty,
                                self.gas_100.tax,
                                self.gas_100.tax_co2,
                                self.gas_100.updated
                            )
                            )
            cur.execute("SELECT updated FROM GasPrice WHERE country=? AND gas_type=?",
                        (self.country, self.gas_95.type_of_gas))
            should_update_gas_95 = False
            i = 0
            while True:
                row = cur.fetchone()
                if (row == None):
                    if (i == 0):
                        should_update_gas_95 = True
                    break
                if (datetime.strptime(row[0], DATE_FORMAT) < datetime.strptime(self.diesel.updated, DATE_FORMAT)):
                    should_update_gas_95 = True
                i += 1
            # 95

            if (should_update_gas_95):
                cur.execute("INSERT INTO GasPrice"
                            "("
                            "country,"
                            "currency,"
                            "gas_type,"
                            "normal,"
                            "price,"
                            "price_neto,"
                            "charge,"
                            "excise_duty,"
                            "tax,"
                            "tax_co2,"
                            "updated"
                            ") VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                            (
                                self.country,
                                self.currency,
                                self.gas_95.type_of_gas,
                                1,
                                self.gas_95.price,
                                self.gas_95.price_neto,
                                self.gas_95.charge,
                                self.gas_95.excise_duty,
                                self.gas_95.tax,
                                self.gas_95.tax_co2,
                                self.gas_95.updated
                            )
                            )

            cur.execute("SELECT updated FROM GasPrice WHERE country=? AND gas_type=?",
                        (self.country, self.ko.type_of_gas))
            should_update_ko = False
            i = 0
            while True:
                row = cur.fetchone()
                if (row == None):
                    if (i == 0):
                        should_update_ko = True
                    break
                if (datetime.strptime(row[0], DATE_FORMAT) < datetime.strptime(self.diesel.updated, DATE_FORMAT)):
                    should_update_ko = True
                i += 1
            if (should_update_ko):
                # kurilno olje
                cur.execute("INSERT INTO GasPrice"
                            "("
                            "country,"
                            "currency,"
                            "gas_type,"
                            "normal,"
                            "price,"
                            "price_neto,"
                            "charge,"
                            "excise_duty,"
                            "tax,"
                            "tax_co2,"
                            "updated"
                            ") VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                            (
                                self.country,
                                self.currency,
                                self.ko.type_of_gas,
                                1,
                                self.ko.price,
                                self.ko.price_neto,
                                self.ko.charge,
                                self.ko.excise_duty,
                                self.ko.tax,
                                self.ko.tax_co2,
                                self.ko.updated
                            )
                            )


with open(rawfile) as file:
    data = json.load(file)

# this line is required to tell the DB which object is the outermost layer
prices_in_slo = Country("Slovenia", data)
print(prices_in_slo)

# this line is required to save the information to the database
prices_in_slo.save_to_database()
