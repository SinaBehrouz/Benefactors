from .postalCodeManager import postalCodeManager
from flask_login import current_user
import json
import requests
import re


class SearchUtil():
    def __init__(self):
        self.pcm = postalCodeManager()
        self.DefPostal = "V5H3Z7"
        self.Key = "AIzaSyCZ2UdTtgsGg7Jbx7UmtnGPFh_pVRi2n4U"
    def get_adv_pc_from_location(self, form):
        '''
            gets the state of the location field in advanced search and return the calculated postal code.
            In case where it is unable to find the postal code it will return -1 as postal code field
        '''
        formPostalCode = form.postalCode.data
        gSuggest = False
        # if len( form.postalCode.data.split(',') ) >= 4:
        #     gSuggest= True

        flash_msg = ""
        if not gSuggest: #get the postal code here
            query_text = re.sub("[ ,.]", "+", formPostalCode)
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query_text}&key={self.Key}"
            response = requests.request("GET", url, headers={}, data = {}).json()
            if response["status"] == "ZERO_RESULTS":
                flash_msg= "Cannot find the provided location - Please Try Again!"
                return (-1, flash_msg)
            postalMap = {}
            for location in response["results"]:
                s =location['formatted_address'].split(',')
                if s[-1].strip().lower() == "canada": #Search only restricted to Canada
                    pc_temp= s[-2].replace(" ", "")[-6:]
                    if pc_temp[:3] not in postalMap:
                        postalMap[ pc_temp[:3] ] = [ pc_temp ]
                    else:
                        postalMap[ pc_temp[:3] ].append(pc_temp)
            most_rep = self.DefPostal
            maxListSize = 0
            if len(postalMap) == 0:
                pc = most_rep
            else:
                for key, List in postalMap.items():
                    if len(List) > maxListSize:
                        maxListSize = len(List)
                        most_rep = key
                pc = postalMap[most_rep][0]
        else:
            parsed_location = formPostalCode.split(',')
            pc = self.pcm.getPCfromCity(parsed_location[-3])
            if not pc:
                if current_user.is_authenticated:
                    flash_msg = 'Unable to find the location - will use the postal code on the account'
                    pc = current_user.postal_code
                else:
                    flash_msg ='Unable to find the location - will use return search based on Vancouver Area'
                    pc = self.DefPostal
        if len(pc) != 6:
            pc = self.DefPostal
        return (pc, flash_msg)
    def get_nearby_locations(self,post):
        '''
            Function to get nearby location on Google map based on post author's postal code and post category
        '''
        postal_code = post.author.postal_code
        category = post.category.name
        google_map = f"https://www.google.com/maps/embed/v1/search?key={self.Key}&q='{category}'+near" + postal_code
        return google_map
