#this module is contains tools for verifying passCodes
from pypostalcode import PostalCodeDatabase


"""
    postalCodeManager provides methods for verifying, finding and searching for
    postal codes in Canada
"""
class postalCodeManager():

    """
        Constructor
    """
    def __init__(self):
        self.pcdb = PostalCodeDatabase()

    """
        Verifies that the provided postal code is valid in Canada

        :param _postalCode: the postal code to be checked
    """
    def verifyPostalCode(self, _postalCode):
        try:
            location = self.pcdb[ _postalCode[:3] ]
        except:
            return False
        return ( _postalCode[3].isnumeric() and _postalCode[4].isalpha() and _postalCode[5].isnumeric() )

    """
        Gets nearby passcodes for a provided base passcode and radius

        :param _postalCode: Base postal code for searching
        :param radius: Search radius
    """
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

    """
        Finds the postal code associated with a city

        :param city: city to be searched for
    """
    def getPCfromCity(self,city):
        city = city.strip()
        all = self.pcdb.find_postalcode()
        for i in all:
            if city.lower() in i.city.lower():
                return i.postalcode
        return None

    """
        Find the city associated with the postal code

        :param _postalCode: target postal code
    """
    def getCityFromPC(self, _postalCode):
        try:
            res = self.pcdb[ _postalCode[:3] ]
        except:
            return "Vancouver, British Columbia, Canada"
        return f"{res.city}, {res.province}, Canada"
