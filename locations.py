#!/usr/bin/env python

import webapp2
import os
import google.appengine.api.urlfetch
import google.appengine.api.memcache

class LocationsHandler(webapp2.RequestHandler):
    def get(self):
        splitted_route = self.request.path.split('/')
        longitude = splitted_route[2]
        latitude = splitted_route[3]

        cache_key = latitude + '_' + longitude

        # try to get the data from the cache
        response_data = google.appengine.api.memcache.get(key=cache_key)

        # The data isn't in the cache therefore fetch and add it to the cache
        if response_data is None:
            # put together the url
            url = 'https://api.forecast.io/forecast/'\
                  + os.environ.get('FORECAST_API_KEY')\
                  + '/'\
                  + latitude\
                  + ','\
                  + longitude\
                  + '?units=si&lang=de'

            response = google.appengine.api.urlfetch.Fetch(url)
            google.appengine.api.memcache.add(key=cache_key,
                                              value=response.content,
                                              time=1800)
            response_data = response.content

        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers.add('Content-Type', 'application/json')
        self.response.write(response_data)

app = webapp2.WSGIApplication([
    ('/locations/.*', LocationsHandler)
], debug=True)
