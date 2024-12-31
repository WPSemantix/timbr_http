#
#             *###              .,              @%             
#       *%##  `#// %%%*  *@     ``              @%             
#        #*.    * .%%%`  @@@@*  @@   @@@@,@@@@  @&@@@@   .&@@@*
#            #%%#   ..   *@     @@  @`  @@` ,@  @%   #@  @@  
#      ,, .,%(##/./%%#,  *@     @@  @`  @@` ,@  @%   #@  @@   
#    ,%##%          ``   `/@@*  @@  @`  @@` ,@  (/@@@#/  @@   
#      ``                                                     
#  ``````````````````````````````````````````````````````````````
#  Copyright (C) 2018-2024 timbr.ai

import requests

def build_url(hostname, port, verify_ssl):
  base_url = 'http'
  base_port = port

  if port == None:
    if verify_ssl:
      base_port = 443
    else:
      base_port = 80

  if verify_ssl:
    base_url = base_url + 's'
  base_url = f'{base_url}://{hostname}:{base_port}/'

  return base_url

def run_query(hostname, ontology, token, query, datasource = None, port = None, nested = 'false', verify_ssl = True, enable_IPv6 = False):
  datasource_addition = ''
  if datasource:
    datasource_addition = f'?datasource={datasource}'
  url = build_url(hostname, port, verify_ssl)
  headers = {'Content-Type': 'application/text', 'x-api-key': token, 'nested': nested, 'Connection': 'close'}
  requests.packages.urllib3.util.connection.HAS_IPV6 = enable_IPv6
  response = requests.post(f'{url}timbr/openapi/ontology/{ontology}/query{datasource_addition}', headers = headers, data = query, verify = verify_ssl)
  return response.json()

# Deprecated - Backward compatibility
def executeTimbrQuery(url, ontology, token, query, override_datasource, nested, verify, enableIPv6):
  datasource_addition = ''
  if override_datasource:
    datasource_addition = f'?datasource={override_datasource}'
  headers = {'Content-Type': 'application/text', 'x-api-key': token, 'nested': nested, 'Connection': 'close'}
  requests.packages.urllib3.util.connection.HAS_IPV6 = enableIPv6
  response = requests.post(f'{url}timbr/openapi/ontology/{ontology}/query{datasource_addition}', headers = headers, data = query, verify = verify)
  return response.json()

def advancedQueryExecute(hostname, port, ontology, token, query, enabled_ssl=True, verify_ssl=True, nested = 'false', enableIPv6 = False, datasource = None):
  baseUrl = "http"
  if enabled_ssl == True:
    baseUrl = baseUrl + "s"
  baseUrl = f"{baseUrl}://{hostname}:{port}/"
  return executeTimbrQuery(baseUrl, ontology, token, query, datasource, nested, verify_ssl, enableIPv6)

def simpleQueryExecution(url, ontology, token, query, datasource = None, nested = 'false'):
  base_url = url
  if not base_url.endswith('/'):
    base_url = f'{url}/'
  return executeTimbrQuery(base_url, ontology, token, query, datasource, nested, True, False)

# Backward compatibility 
def executeQuery(hostname, port, ontology, token, query, enabled_ssl=True, verify_ssl=True, nested = 'false'):
  baseUrl = "http"
  if enabled_ssl == True:
    baseUrl = baseUrl + "s"
  baseUrl = f"{baseUrl}://{hostname}:{port}/"
  return legacyExecuteTimbrQuery(baseUrl, ontology, token, query, nested, verify_ssl)

def legacyExecuteTimbrQuery(url, ontology, token, query, nested, verify):
  post_data = {'ontology_name': ontology, 'query': query}
  headers = {'Content-Type': 'application/json', 'x-api-key': token, 'nested': nested}
  response = requests.post(url + "timbr/api/query/", headers = headers, json = post_data, verify = verify)
  return response.json()