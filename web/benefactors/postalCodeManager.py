#this module is contains tools for verifying passCodes
from pypostalcode import PostalCodeDatabase

class postalCodeManager():
    def __init__(self):
        self.pcdb = PostalCodeDatabase()

    def verifyPostalCode(self, _passcode):
        try:
            location = self.pcdb[ _passcode[:3] ]
        except:
            return False
        return ( _passcode[3].isnumeric() and _passcode[4].isalpha() and _passcode[5].isnumeric() )

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
