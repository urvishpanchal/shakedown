# -*- coding: utf-8 -*-
# Copyright (c) 2015 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.


import urllib2, json, base64, csv, filesys


class TestrailClient:
	def __init__(self, base_url):
		self.user = ''
		self.password = ''
		if not base_url.endswith('/'):
			base_url += '/'
		self.__url = base_url + 'index.php?/api/v2/'

	#
	# Send Get
	#
	# Issues a GET request (read) against the API and returns the result
	# (as Python dict).
	#
	# Arguments:
	#
	# uri                 The API method to call including parameters
	#                     (e.g. get_case/1)
	#
	def send_get(self, uri):
		return self.__send_request('GET', uri, None)

	#
	# Send POST
	#
	# Issues a POST request (write) against the API and returns the result
	# (as Python dict).
	#
	# Arguments:
	#
	# uri                 The API method to call including parameters
	#                     (e.g. add_case/1)
	# data                The data to submit as part of the request (as
	#                     Python dict, strings must be UTF-8 encoded)
	#
	def send_post(self, uri, data):
		return self.__send_request('POST', uri, data)

	def __send_request(self, method, uri, data):
		url = self.__url + uri
		request = urllib2.Request(url)
		if (method == 'POST'):
			request.add_data(json.dumps(data))
		auth = base64.b64encode('%s:%s' % (self.user, self.password))
		request.add_header('Authorization', 'Basic %s' % auth)
		request.add_header('Content-Type', 'application/json')

		e = None
		try:
			response = urllib2.urlopen(request).read()
		except urllib2.HTTPError as e:
			response = e.read()

		if response:
			result = json.loads(response)
		else:
			result = {}

		if e != None:
			if result and 'error' in result:
				error = '"' + result['error'] + '"'
			else:
				error = 'No additional error message received'
			raise APIError('TestRail API returned HTTP %s (%s)' %
				(e.code, error))

		return result

class APIError(Exception):
	pass

def lookup_test_case(case_id):
    f = open("testrail_mapping.csv")
    for row in csv.reader(f):
        if row[0] == str(case_id):
            return row[1].split()
    return 'none'

def collect(config, filter):
    client = TestrailClient(config['testrail']['url'])
    client.user = config['testrail']['username']
    client.password = config['testrail']['password']
    runId = config['testrail']['run_id']
    uri = "get_tests/"+str(runId)
    run = client.send_get(uri)
    for test in run:
        if str(test['case_id']) == str(filter[0]):
            case = lookup_test_case(test['case_id'])
            return filesys.collect(config,case)
