#this module is contains tools for verifying passCodes
from pypostalcode import PostalCodeDatabase

class postalCodeManager():
    def __init__(self):
        self.pcdb = PostalCodeDatabase()

    def verifyPostalCode(self, _postalCode):
        try:
            location = self.pcdb[ _postalCode[:3] ]
        except:
            return False
        return ( _postalCode[3].isnumeric() and _postalCode[4].isalpha() and _postalCode[5].isnumeric() )

    def getNearybyPassCodes(self, _passcode, radius):
        pc = _passcode[:3]
        radius = radius
        results = self.pcdb.get_postalcodes_around_radius(pc, radius)
        nearby_postal_codes = set()
        for r in results:
            nearby_postal_codes.add(r.postalcode + '%')
        nearby_postal_codes = list(nearby_postal_codes)
        nearby_postal_codes = tuple(nearby_postal_codes)
        return nearby_postal_codes
    def getPCfromCity(self,city):
        city = city.strip()
        all = self.pcdb.find_postalcode()
        for i in all:
            if city.lower() in i.city.lower():
                return i.postalcode
        return None
    def getCityFromPC(self, _postalCode):
        try:
            res = self.pcdb[ _postalCode[:3] ]
        except:
            return "Vancouver, British Columbia, Canada"
        return f"{res.city}, {res.province}, Canada"
