#!/usr/bin/env python3
import requests as r #import installed requests module
from requests.exceptions import HTTPError, JSONDecodeError #import requests exceptions
from requests.compat import urljoin #could be usefull to create url…
import json as js

class Client:
    def __init__(self, baseUrl: str, defaultProtocol: str="http") :
        self.__baseUrl__ = baseUrl #nom de domaine / Domain name
        self.__defaultProtocol__ = defaultProtocol #Request protocol if not specified
        self.__r__ = None #Server response
        self.__error__ = None #errors

    #Changes the base url
    def set_baseUrl(self, baseUrl: str) :
        self.__baseUrl__ = baseUrl

    #Creates a url out of a Client object, a route and a protocol
    def make_url(self, route: str, protocol: str | None = None) -> str :
        if protocol == None:
            protocol = self.__defaultProtocol__
        return urljoin(protocol + "://" + self.__baseUrl__, route)

    #issues an http get request
    def get(self, route: str, payload: dict = {}, protocol: str | None = None) -> bool :
        res = True
        try :
            # Stores in __r__ the response to the query
            self.__r__ = r.get(self.make_url(route, protocol), params=payload)
            # Deletes the last error (if an error is raised this is not executed)
            self.__error__ = None
        #possible errors
        except HTTPError as http_err:
            self.__error__ = f'HTTP error occurred: {http_err}'
            self.__r__ = None
            res = False
        except Exception as err:
            self.__error__ = f'Other error occurred: {err}'
            self.__r__ = None
            res = False
        return res

    #issues an http post request
    def post(self, route: str, data = None, protocol: str | None = None) -> bool :
        res = True
        try :
            # Stores in __r__ the response to the query
            url = self.make_url(route, protocol)
            print(url)
            if data is None :
                self.__r__ = r.post(url)
            else :
                self.__r__ = r.post(url, json=data)
            # Deletes the last error (if an error is raised this is not executed)
            self.__error__ = None
        #possible errors
        except HTTPError as http_err:
            self.__error__ = f'HTTP error occurred: {http_err}'
            self.__r__ = None
            res = False
        except Exception as err:
            self.__error__ = f'Other error occurred: {err}'
            self.__r__ = None
            res = False
        return res

    #issues an http delete request
    def delete(self, route: str, protocol: str | None = None) -> bool :
        res = True
        try :
            # Stores in __r__ the response to the query
            self.__r__ = r.delete(self.make_url(route, protocol))
            # Deletes the last error (if an error is raised this is not executed)
            self.__error__ = None
        #possible errors
        except HTTPError as http_err:
            self.__error__ = f'HTTP error occurred: {http_err}'
            self.__r__ = None
            res = False
        except Exception as err:
            self.__error__ = f'Other error occurred: {err}'
            self.__r__ = None
            res = False
        return res

    #returns the last response to a succesful query
    def lr(self) -> r.Response :
        return self.__r__

    #returns the last error raised by a query
    def lr_error(self) -> str :
        return self.__error__

    def lr_status_code(self) -> int | None :
        res = None
        if self.__r__ != None:
            res = self.__r__.status_code
        return res

    def lr_headers(self) -> dict | None :
        res = None
        if self.__r__ != None:
            res = self.__r__.headers
        return res

    def lr_response(self, json: bool = False) -> str | dict | None :
        res = None
        if self.__r__ != None:
            if json :
                try :
                    res = self.__r__.json()
                except JSONDecodeError :
                    res = "Cannot decode json from response"
            else :
                res = self.__r__.text
        return res

    def lr_redirections(self) -> str :
        if len(self.__r__.history) == 0 :
            return "Pas de redirections"
        return "Redirections : " + ", ".join(str(resp.headers["Location"]) for resp in self.__r__.history)