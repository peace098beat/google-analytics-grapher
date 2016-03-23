"""A simple example of how to access the Google Analytics API."""

import argparse

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

import sys
import os

print "---- GoogleAnalyticsManager ----"
print __file__
print sys.argv[0]
print os.path.dirname(__file__)



weddingmovie = True

def get_service(api_name, api_version, scope, key_file_location,
                service_account_email):
    """Get a service that communicates to a Google API.

    Args:
      api_name: The name of the api to connect to.
      api_version: The api version to connect to.
      scope: A list auth scopes to authorize for the application.
      key_file_location: The path to a valid service account p12 key file.
      service_account_email: The service account email address.

    Returns:
      A service that is connected to the specified API.
    """

    # Read Key FIle (.p12)
    f = open(key_file_location, 'rb')
    key = f.read()

    print 'key file location'
    print key
    print type(key)

    f.close()

    credentials = SignedJwtAssertionCredentials(service_account_email, key,
                                                scope=scope)

    http = credentials.authorize(httplib2.Http())

    # Build the service object.
    service = build(api_name, api_version, http=http)

    return service


def get_first_profile_id(service):
    # Use the Analytics service object to get the first profile id.

    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
        # Get the first Google Analytics account.
        account = accounts.get('items')[0].get('id')
        # print 'account id: %s' % account

        # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(
            accountId=account).execute()
        # print 'properties : %s' % properties

        if properties.get('items'):
            # Get the first property id.
            property = properties.get('items')[0].get('id')
            # print 'property : %s' % property

            # Get a list of all views (profiles) for the first property.
            profiles = service.management().profiles().list(
                accountId=account,
                webPropertyId=property).execute()

            if profiles.get('items'):
                # for item in profiles.get('items'):
                #     print item.get('id')
                # return the first view (profile) id.
                return profiles.get('items')[0].get('id')
            # else:
            #     print 'Not profiles items : %d' % 89190887
                # id = '89190887'
                # return id


    return None


def get_results(service, profile_id):
    # Use the Analytics Service Object to query the Core Reporting API
    # for the number of sessions within the past seven days.
    return service.data().ga().get(
        ids='ga:' + profile_id,
        start_date='7daysAgo',
        end_date='today',
        metrics='ga:sessions').execute()


def print_results(results):
    # Print data nicely for the user.
    if results:
        print 'Type results: %s' % type(results)
        print 'View (Profile): %s' % results.get('profileInfo').get('profileName')
        print 'Total Sessions: %s' % results.get('rows')[0][0]
        import pprint
        pprint.pprint(results)

    else:
        print 'No results found'


def initGoogleApis(email=None, keyfile=None):
    print 'initGoogleApis'
    # Define the auth scopes to request.
    scope = ['https://www.googleapis.com/auth/analytics.readonly']

    # service account email and relative location of your key file.
    if email is None:
        # service_account_email = '321268087270-c6nrdep9v3suagivv821q16pi6pkadcs@developer.gserviceaccount.com'
        service_account_email = '1012296075859-srmal3ibkuum4mea40vs9qbols6b9g9a@developer.gserviceaccount.com' # wedding movie
    else:
        service_account_email = email

    # service account email and relative location of your key file.
    if keyfile is None:
        # key_file_location = 'client_secrets.p12'
        key_file_location = 'client_secrets_wm.p12'
    else:
        key_file_location = keyfile

    # Authenticate and construct service.
    service = get_service('analytics', 'v3', scope, key_file_location, service_account_email)

    # ------------------------------------ #
    if weddingmovie:
        profile = '98501400'
    else:
        profile = get_first_profile_id(service)

    print "init Google Apis : service : %s" % service
    print "init Google Apis : profile : %s" % profile

    return service, profile


def main():
    # Define the auth scopes to request.
    scope = ['https://www.googleapis.com/auth/analytics.readonly']

    # Use the developer console and replace the values with your
    # service account email and relative location of your key file.
    # service_account_email = '321268087270-c6nrdep9v3suagivv821q16pi6pkadcs@developer.gserviceaccount.com' # fififactory hatena
    service_account_email = '1012296075859-srmal3ibkuum4mea40vs9qbols6b9g9a@developer.gserviceaccount.com' # wedding movie
    # key_file_location = 'client_secrets.p12'
    key_file_location = 'client_secrets_wm.p12'

    # Authenticate and construct service.
    service = get_service('analytics', 'v3', scope, key_file_location,
                          service_account_email)
    print 'service : %s' % service

    profile = get_first_profile_id(service)
    print 'profile : %s' % (profile)

    print_results(get_results(service, profile))


if __name__ == '__main__':
    main()
