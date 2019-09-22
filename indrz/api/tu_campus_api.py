import json
import os
from collections import namedtuple
from urllib import parse
from concurrent.futures import ThreadPoolExecutor

import requests


SearchResult = namedtuple('SearchResult', ['staff', 'organizations'])


class TuCampusAPI:
    """
    Wrapper for AAU API
    """

    API_PROTOCOL = 'https'
    API_DOMAIN = 'tiss.tuwien.ac.at/api'

    ORGUNIT = '/orgunit/v22/code/E259-01?persons=false'
    ORGUNIT_ID = '/orgunit/v22/id/5822?persons=false'

    # Orgeinheiten - Nummer
    # ORGUNIT_NUM = '/api/orgunit/v22/number/E193-02?persons=true'
    ORGUNIT_NUM = '/orgunit/v22/number'

    # Liefert alle aktiven Organisationseinheiten der TU-Wien
    ORG_ALL = '/orgunit/v22/organigramm'

    # Ergebnis der Suchanfrage von Orgeinheiten
    ORG_SEARCH = '/orgunit/v22/osuche/?q='

    # Detaildaten einer Person auf Basis der TISS-ID
    PERSON_ID = '/person/v22/id/139234'

    # Detaildaten eines Studenten auf Basis der Matrikelnummer
    PERSON_MAT_NUM = '/person/v22/mnr/00427547'

    # Detaildaten einer Person auf Basis der OID
    PERSON_OID = '/person/v22/oid/258593'

    # Ergebnis der Suchanfrage von Personen

    # PERSON_SEARCH = '/api/person/v22/psuche/?q=somename'
    PERSON_SEARCH = '/person/v22/psuche/'


    def filter_no_roomkey(self, data, source):

        newres = []

        for result in data:
            # source person search
            if 'employee' in result:
                if result['employee']:
                    for d in result['employee']:
                        if 'room' in d:
                            if d['room']['room_code']:
                                name = result['first_name'] + " " + result['last_name']
                                res = {'name': name, 'roomcode': d['room']['room_code'], "src": source}
                                newres.append(res)
                            else:
                                continue
            # source organization search
            if 'employees' in result:
                for employee in result['employees']:
                    if 'function' in employee:
                        if employee['function'] == 'Sekretariat':
                            if 'room_code' in employee:
                                r_code = employee['room_code']
                                name = result['first_name'] + " " + result['last_name']
                                res = {'name': name, 'roomcode': r_code, "src": source}
                                newres.append(res)
                            else:
                                continue
        if newres:
            return newres
        else:
            return []

    def build_url(self, path, query_data=None):
        """
        Utility function. Constructs full url to access API methods
        :param path: path to specific method
        :param query_data: dictionary of query paramerets
        :return: URL string
        """
        query_data = query_data or {}
        url = parse.urlunsplit((self.API_PROTOCOL, self.API_DOMAIN,
                                path,
                                query_data,
                                ''))
        return url


    def search_staff(self, name):
        """
        Searches for staff by name
        :param name:
        :return: list of dicts
        """

        person_search = "q=" + name
        print("final url persons ", self.build_url(self.PERSON_SEARCH, person_search))
        res = requests.get(self.build_url(self.PERSON_SEARCH, person_search))

        print("rest ", res.status_code, res.content)
        if res.status_code == 200:

            print(res.json())

            res_json = res.json()

            people_with_rooms_assigned = self.filter_no_roomkey(res_json['results'], source="external person api")
            if people_with_rooms_assigned:
                return people_with_rooms_assigned
            else:
                return None
                # return {"error": "no room assigned", "method": "search_staff"}
        else:
            return None
            # return {"error": "no data found", "method": "search_staff"}

    # def search_staff_unmodified(self, name):
    #     """
    #     Searches for staff by name
    #     :param name:
    #     :return: list of dicts
    #     """
    #     data = {
    #         'name': name
    #     }
    #
    #     res = requests.get(self.build_url(self.STAFF_SEARCH_PATH, data))
    #
    #     if res.status_code == 200:
    #         return res.json()
    #     else:
    #         return None
            # return {"error": "no data found", "method": "search_staff"}


    # def search_rooms(self, *, room_id=None, room_number=None, description=None,
    #                  ou=None):
    #     """
    #     Searches for rooms by either room ID
    #     or room number
    #     or description
    #     or organization
    #
    #     Arguments are mutually exclusive
    #     :param room_id:
    #     :param room_number:
    #     :param description:
    #     :param ou:
    #     :return: list of dicts
    #     """
    #
    #     if room_id:
    #         url = '%s/%s' % (self.ROOMS_SEARCH_PATH, room_id)
    #         return requests.get(self.build_url(url)).json()
    #
    #     for key, value in (('roomnumber', room_number),
    #                        ('description', description),
    #                        ('ou', ou)):
    #         if value:
    #             data[key] = value
    #
    #     res = requests.get(self.build_url(self.ROOMS_SEARCH_PATH))
    #
    #     if res.status_code == 200:
    #
    #         fa = self.filter_no_roomkey(res.json(), source="external rooms api")
    #
    #         if fa:
    #             return fa
    #         else:
    #             return None
    #     else:
    #         return None
    #         # return {"error": "no data found", "method": "search_rooms"}
    #
    # def search_rooms_simple(self, name):
    #     """
    #     Simplified version of self.search_rooms() for usage in
    #     ThreadPoolExecutor.
    #
    #     Accepts single argument `name` that is passed as `description` argument
    #     to self.search_rooms()
    #     :param name:
    #     :return: list of dicts
    #     """
    #     return self.search_rooms(description=name)

    def search_organizations(self, name):
        """
        Searches for organization by name
        :param name:
        :return: list of dicts
        """
        # ORG_SEARCH = '/api/orgunit/v22/osuche/?q='

        res = requests.get(self.build_url(self.ORG_SEARCH, name))

        if res.status_code == 200:

            r = res.json()

            codes = []
            if r['results']:
                for result in r['results']:
                    if 'code' in result:
                        codes.append(result['code'])


            org_sekretariate_roomcodes = []
            for code in codes:
                final = code + "?persons=true"
                org_data = requests.get(self.build_url(self.ORGUNIT_NUM, final))

                jj = json.loads(org_data.json())

                if 'employees' in jj:
                    for employee in jj['employees']:
                        if 'function' in employee:
                            if employee['function'] == 'Sekretariat':
                                if 'room_code' in employee:
                                    r_code = employee['room_code']
                                    org_sekretariate_roomcodes.append(r_code)



                # ORGUNIT_NUM = '/api/orgunit/v22/number/E193-02?persons=true'


            fa = self.filter_no_roomkey(r['results'], source="external organization api")

            if fa:
                return fa
            else:
                return None
        else:
            return None
            # return {"error": "no data found", "method": "search_organizations"}


    def search(self, name):
        """
        Searches for staff, rooms and organizations at the same time.
        Returns SearchResult named tuple with three result sets
        :param name:
        :return:
        """
        pool = ThreadPoolExecutor(3)
        funcs = (self.search_staff,
                 self.search_organizations)
        futures = [pool.submit(func, name) for func in funcs]

        aau_api_search = SearchResult(*[future.result() for future in futures])



        if any(aau_api_search):
            return aau_api_search
        else:
            return None



def api_res_source(x):
    result_type = ''

    # if x.rooms:
    #     result_type = 'rooms'
    #     return result_type
    if x.staff:
        result_type = 'staff'
        return result_type
    elif x.organizations:
        result_type = 'organizations'
        return result_type
    else:
        return None


