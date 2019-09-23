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
    ORGUNIT_NUM = '/orgunit/v22/number/'

    # Liefert alle aktiven Organisationseinheiten der TU-Wien
    ORG_ALL = '/orgunit/v22/organigramm'

    # Ergebnis der Suchanfrage von Orgeinheiten
    # ?q=
    ORG_SEARCH = '/orgunit/v22/osuche/'

    # Detaildaten einer Person auf Basis der TISS-ID
    PERSON_ID = '/person/v22/id/139234'

    # Detaildaten eines Studenten auf Basis der Matrikelnummer
    PERSON_MAT_NUM = '/person/v22/mnr/00427547'

    # Detaildaten einer Person auf Basis der OID
    PERSON_OID = '/person/v22/oid/258593'

    # Ergebnis der Suchanfrage von Personen

    # PERSON_SEARCH = '/api/person/v22/psuche/?q=somename'
    PERSON_SEARCH = '/person/v22/psuche/'

    def gen_res(self, result, source, r_code):
        name = result['first_name'] + " " + result['last_name']
        res = {'name': name, 'roomcode': r_code, "src": source}
        return res

    # def filter_no_roomkey(self, data, source):
    #
    #     newres = []
    #
    #     for result in data:
    #         # source person search
    #
    #         if source == "external person api":
    #             if 'employee' in result:
    #                 if result['employee']:
    #                     for employee in result['employee']:
    #                         if 'room' in employee:
    #                             if employee['room']['room_code']:
    #                                 r_code = employee['room']['room_code']
    #                                 newres.append(self.gen_res(result,source, r_code))
    #                                 print("in persons ", len(newres))
    #         if source == "external organization api":
    #             r_code = result['room_code']
    #             newres.append(self.gen_res(result, source, r_code))
    #             print("in orgs len ", len(newres))
    #
    #     print("FINAL len results is ", len(newres))
    #     if newres:
    #         return newres
    #     else:
    #         return []

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
        res = requests.get(self.build_url(self.PERSON_SEARCH, person_search))
        source = "external person api"

        if res.status_code == 200:

            res_json = res.json()

            people_with_rooms_assigned = []

            for result in res_json['results']:
                if 'employee' in result:
                    if result['employee']:
                        if len(result['employee']) > 1:
                            employee = result['employee'][0]
                            # take first room person has because this person is assigned more than one room
                            if 'room' in employee:
                                if employee['room']['room_code']:
                                    r_code = employee['room']['room_code']
                                    name_concat = result['first_name'] + " " + result['last_name']
                                    f_res = {'name': name_concat, 'roomcode': r_code, "src": source}
                                    people_with_rooms_assigned.append(f_res)
                        if len(result['employee']) == 1:
                            employee = result['employee']
                            if 'room' in employee:
                                if employee['room']['room_code']:
                                    r_code = employee['room']['room_code']
                                    name_concat = result['first_name'] + " " + result['last_name']
                                    f_res = {'name': name_concat, 'roomcode': r_code, "src": source}
                                    people_with_rooms_assigned.append(f_res)

            # people_with_rooms_assigned = self.filter_no_roomkey(res_json['results'], source="external person api")

            if people_with_rooms_assigned:
                return people_with_rooms_assigned
            else:
                return None
                # return {"error": "no room assigned", "method": "search_staff"}
        else:
            return None
            # return {"error": "no data found", "method": "search_staff"}


    def search_organizations(self, name):
        """
        Searches for organization by name
        :param name:
        :return: list of dicts
        """
        # ORG_SEARCH = '/api/orgunit/v22/osuche/?q='

        se = "q=" + name
        source = "external organization api"

        res = requests.get(self.build_url(self.ORG_SEARCH, se))

        if res.status_code == 200:

            r = res.json()

            codes = []
            if r['results']:
                for result in r['results']:
                    if 'code' in result:
                        codes.append(result['code'])

            org_sekretariate_roomcodes = {'results': []}


            newres = []
            for code in codes:
                # https://tiss.tuwien.ac.at/api/orgunit/v22/number/E020/?persons=true
                org_resp = requests.get(self.build_url(self.ORGUNIT_NUM + code, "persons=true"))
                org_data = org_resp.json()

                if 'employees' in org_data:
                    for employee in org_data['employees']:
                        if 'function' in employee:
                            if employee['function'] == 'Sekretariat':
                                if 'room_code' in employee:
                                    r_code = employee['room_code']
                                    # name = employee['first_name'] + " " + employee['last_name']
                                    # res = {'name': name, 'roomcode': r_code, "src": 'external organization api'}
                                    # org_sekretariate_roomcodes['results'].append(employee)

                                    name_concat = employee['first_name'] + " " + employee['last_name']
                                    f_res = {'name': name_concat, 'roomcode': r_code, "src": source}
                                    # people_with_rooms_assigned.append(f_res)

                                    newres.append(f_res)
                                    print("in orgs len ", len(newres))


            # fa = self.filter_no_roomkey(org_sekretariate_roomcodes['results'], source="external organization api")

            if newres:
                return newres
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


