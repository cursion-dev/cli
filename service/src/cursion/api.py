import requests, json, os, time
from dotenv import load_dotenv
from pathlib import Path
from rich import print as rprint

env_file = Path(str(Path.home()) + '/cursion/.env')

load_dotenv(dotenv_path=env_file)

# import env vars
CURSION_API_BASE_URL = f'{os.getenv('API_ROOT')}/v1/ops'
CURSION_CLIENT_BASE_URL = os.getenv('CLIENT_ROOT')
CURSION_API_TOKEN = f'Token {os.getenv('API_KEY')}'
headers = {
   "content-type": "application/json",
   "Authorization" : CURSION_API_TOKEN
}




def format_response(response: dict) -> dict:

    # checking response for error
    success = True
    if not str(response.status_code).startswith('2'):
        success = False

    # retrieve response data
    json_response = response.json()

    # format response
    resp = {
        'success': success,
        'data': json_response
    }

    return resp




def check_headers(api_key:str = None):

    # check headers for API KEY
    if 'None' in headers["Authorization"] or \
        len(headers["Authorization"]) < 20:

        # check if API_KEY was passed
        if api_key is None:
            rprint(
                '[red bold]' + u'\u2718' + '[/red bold]' +
                f' please pass --api-key=<api-key>'
            )
            return None

        # updated header if api_key is present
        headers["Authorization"] = f'Token {api_key}'
        return headers

    # return unchanged headers 
    else:
        return headers




def check_api_url(url: str=None, api_root:str = None):

    # check api_root for uri
    if 'None' in url:

        # check if API_ROOT was passed
        if api_root is None:
            rprint(
                '[red bold]' + u'\u2718' + '[/red bold]' +
                f' please pass --api-root=<private-api-root>'
            )
            return None

        # updated url if api_root is present
        url = url.replace('None', api_root)
        return url

    # return unchanged headers
    else:
        return url




def api_add_site(*args, **kwargs):

    """ 
    This Endpoint will create a `Site` object 
    with the root url being the passed "site_url". 
    Also initiates Crawler() which creates new `Pages` 
    and new `Scans` for each new `Page`.
    """

    # get kwargs
    site_url = kwargs.get('site_url')
    page_urls = kwargs.get('page_urls')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/site'

    data = {
        "site_url": site_url,
        "page_urls": page_urls if page_urls is not None else None
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)
        
    # send the request
    res = requests.post(
        url=url, 
        headers=headers, 
        data=json.dumps(data)
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_crawl_site(*args, **kwargs):

    """
    This Endpoint will crawl the site for any new `Pages` not 
    already recorded (Stopping once "Account.max_pages" has been reached), 
    and auto create a `Scan` for each new `Page` it records.
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/site/{site_id}/crawl' 

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)

    # send the request
    res = requests.post(
        url=url, 
        headers=headers, 
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_get_sites(*args, **kwargs):

    """
    This endpoint will return the `Site` object 
    associated with the passed "site_id"
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/site'

    params = {
        "site_id": site_id,
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)

    # send the request
    res = requests.get(
        url=url, 
        headers=headers, 
        params=params
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_delete_site(*args, **kwargs):

    """
    This endpoint will delete the `Site` object 
    associated with the passed "site_id" /site/<site_id>
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/site/{site_id}'

    # check headers for API KEY
    headers = check_headers(api_key=api_key)
    
    # check url for API ROOT
    url = check_api_url(url, api_root)

    # send the request
    res = requests.delete(
        url=url, 
        headers=headers, 
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_add_page(*args, **kwargs):

    """
    This endpoint will create a new `Page` 
    object associated with the passed "site_id". 
    Also creates an initial `Scan` object for each new `Page`
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    page_url = kwargs.get('page_url')
    page_urls = kwargs.get('page_urls')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/page'

    data = {
        "site_id": site_id,   
        "page_url": page_url if page_url is not None else None,
        "page_urls": page_urls if page_urls is not None else None, 
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)

    # send the request
    res = requests.post(
        url=url, 
        headers=headers, 
        data=json.dumps(data)
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_get_pages(*args, **kwargs):

    """ 
    This endpoint will retrieve a list of `Page` 
    objects filtered by the passed "site_id".
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    page_id = kwargs.get('page_id')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/page'

    params = {
        "site_id": site_id,
        "page_id": page_id, # OPTIONAL for returning a specific Page
        "lean": "true" 
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)

    # send the request
    res = requests.get(
        url=url, 
        headers=headers, 
        params=params
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_delete_page(*args, **kwargs):

    """
    This endpoint will delete the `Page` object 
    associated with the passed "page_id" /page/<page_id>
    """

    # get kwargs
    page_id = kwargs.get('page_id')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/page/{page_id}'

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)
    
    # send the request
    res = requests.delete(
        url=url, 
        headers=headers, 
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_scan_site(*args, **kwargs):

    """ 
    This endpoint will create a new `Scan` for each 
    `Page` associated with the passed "site_id".
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/scan'

    data = {
        "site_id": site_id 
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)

    # send the request
    res = requests.post(
        url=url, 
        headers=headers, 
        data=json.dumps(data)
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_scan_page(*args, **kwargs):

    """
    This Endpoint will create a `Scan` for 
    only the passed "page_id" 
    """

    # get kwargs
    page_id = kwargs.get('page_id')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/scan'

    data = {
        "page_id": page_id
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)

    # send the request
    res = requests.post(
        url=url, 
        headers=headers, 
        data=json.dumps(data)
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_get_scans(*args, **kwargs):

    """
    This Endpoint will retrieve one or more `Scans` for 
    only the passed "page_id" - recommend using "lean=true"
    """

    # get kwargs
    page_id = kwargs.get('page_id')
    scan_id = kwargs.get('scan_id')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/scan'

    params = {
        'scan_id': scan_id,  # OPTIONAL for returning a specific Scan
        'page_id': page_id,
        'lean': 'true'
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)

    # send the request
    res = requests.get(
        url=url, 
        headers=headers, 
        params=params
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_test_page(*args, **kwargs):

    """
    This Endpoint will create a `Test` for only the passed "page_id".
    Current version requires both the "pre_scan" and "post_scan" to be 
    passed in the API call.
    """

    # get kwargs
    page_id = kwargs.get('page_id')
    pre_scan = kwargs.get('pre_scan')
    post_scan = kwargs.get('post_scan')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/test'

    data = {
        "page_id": page_id,
        "pre_scan": pre_scan, 
        "post_scan": post_scan,
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)

    # send the request
    res = requests.post(
        url=url, 
        headers=headers, 
        data=json.dumps(data)
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_get_tests(*args, **kwargs):

    """
    This Endpoint will retrieve one or more `Tests` for 
    only the passed "page_id" - recommend using "lean=true"
    """

    # get kwargs
    page_id = kwargs.get('page_id')
    test_id = kwargs.get('test_id')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/test'

    params = {
        'test_id': test_id, 
        'page_id': page_id,
        'lean': 'true'
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)

    # send the request
    res = requests.get(
        url=url, 
        headers=headers, 
        params=params
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_get_cases(*args, **kwargs):

    """
    This Endpoint will retrieve one or more `Cases` for 
    only the passed "site_id"
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    case_id = kwargs.get('case_id')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/case'

    params = {
        'case_id': case_id, 
        'site_id': site_id,
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)

    # send the request
    res = requests.get(
        url=url, 
        headers=headers, 
        params=params
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_get_caseruns(*args, **kwargs):

    """
    This Endpoint will retrieve one or more `CaseRuns` for 
    only the passed "site_id"
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    caserun_id = kwargs.get('caserun_id')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/caserun'

    params = {
        'caserun_id': caserun_id,
        'site_id': site_id,
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)

    # send the request
    res = requests.get(
        url=url, 
        headers=headers, 
        params=params
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_add_caserun(*args, **kwargs):

    """
    This Endpoint will create and run a new `CaseRuns` 
    for the passed "site_id" & "case_id"
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    case_id = kwargs.get('case_id')
    updates = kwargs.get('updates')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/caserun'

    data = {
        'case_id': case_id,
        'site_id': site_id,
        'updates': updates
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)

    # send the request
    res = requests.post(
        url=url, 
        headers=headers,
        data=json.dumps(data)
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_get_flows(*args, **kwargs):

    """
    This Endpoint will one or more `Flows` for 
    only the passed "flow_id"
    """

    # get kwargs
    flow_id = kwargs.get('flow_id')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/flow'

    params = {
        'flow_id': flow_id,
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)

    # send the request
    res = requests.get(
        url=url, 
        headers=headers, 
        params=params
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_get_flowruns(*args, **kwargs):

    """
    This Endpoint will retrieve one or more `FlowRuns` for 
    only the passed "site_id"
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    flowrun_id = kwargs.get('flowrun_id')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/flowrun'

    params = {
        'flowrun_id': flowrun_id,
        'site_id': site_id,
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)

    # send the request
    res = requests.get(
        url=url, 
        headers=headers, 
        params=params
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_add_flowrun(*args, **kwargs):

    """
    This Endpoint will create a new `FlowRun` 
    for the passed "site_id" & "flow_id"
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    flow_id = kwargs.get('flow_id')
    api_key = kwargs.get('api_key')
    api_root = kwargs.get('api_root')

    # setup configs
    url = f'{CURSION_API_BASE_URL}/flowrun'

    data = {
        'flow_id': flow_id,
        'site_id': site_id,
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # check url for API ROOT
    url = check_api_url(url, api_root)

    # send the request
    res = requests.post(
        url=url, 
        headers=headers,
        data=json.dumps(data)
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def wait_for_completion(ids: list, obj: str, api_root: str=None) -> None:

    """ 
    This method waits for either a set of `Scans` & `Tests` or 
    `CaseRun` & `FlowRun` objects finish running - or timesout 
    at max_wait_time (900s)
    """

    max_wait_time = 900
    wait_time = 0
    completions = []
    log_index = 0
    while (len(completions) != len(ids)) and wait_time < max_wait_time:
        # sleeping for 10 seconds
        time.sleep(10)
        wait_time += 15
        # checking status of obj
        for id in ids:
            if obj == 'scan':
                time_complete = api_get_scans(scan_id=id, page_id=None, api_root=api_root)['data']['time_completed']
            if obj == 'test':
                time_complete = api_get_tests(test_id=id, page_id=None, api_root=api_root)['data']['time_completed']
            if obj == 'caserun':
                time_complete = api_get_caseruns(caserun_id=id, api_root=api_root)['data']['time_completed']
            if obj == 'flowrun':
                flowrun = api_get_flowruns(flowrun_id=id, api_root=api_root)['data']
                time_complete = flowrun['time_completed']
                # print new logs
                for i in range(log_index, (len(flowrun['logs']))):
                    rprint(f'  [blue bold]{flowrun['logs'][i]['timestamp']}[/blue bold]  |  {flowrun['logs'][i]['message']}')
                # set new log index to len(logs)
                log_index = len(flowrun['logs'])
            
            # alerting completion
            if time_complete is not None and id not in completions:
                rprint('\n[green bold]' + u'\u2714' + '[/green bold]' + f' {obj} completed -> {id}')
                completions.append(id)

    return None




def api_test_site(
        site_id: str,
        max_wait_time: int=120,
        threshold: int=95,
        api_key: str=None,
        api_root: str=None,
        client_root: str=None
    ):
    
    """ 
    This method will run a full `Test` for the `Site`
    asocaited with the passed id's. 

    Steps:
        1. Determine if testing full site or page
        2. Wait for `Site` to be available
        3. Get all `Pages` for associated `Site`
        4. Get all "pre_scan" id's for each `Page`
        5. Check for all "pre_scan" completion
        6. Create new "post_scans" for each `Page`
        7. Check for all "post_scan" completion
        8. Create new `Test` for each `Page`
        9. Check for all `Test` completion
    """

    # 1. get the site
    site = api_get_sites(
        site_id=site_id, 
        api_key=api_key, 
        api_root=api_root
    )['data']

    # 2. Check for crawl completion
    wait_time = 0
    site_status = 500
    print(f'checking site availablity...')
    while str(site_status).startswith('5') and wait_time < max_wait_time:
        # sleeping for 5 seconds
        time.sleep(5)
        wait_time += 5
        # check site status
        site_status = requests.get(url=site['site_url']).status_code
    
    # determine if timeout 
    if wait_time >= max_wait_time:
        rprint(
            '[red bold]' + u'\u2718' + '[/red bold]' + 
            ' max wait time reached - proceeding with caution...'
        )
    else:
        rprint(
            '[green bold]' + u'\u2714' + '[/green bold]' 
            + ' site is available'
        )

    # 3. Get all `Pages` for associated `Site` 
    print(f'\nretrieving pages...')
    pages = api_get_pages(
        site_id=str(site['id']), 
        api_key=api_key,
        api_root=api_root
    )['data']['results']
    rprint('[green bold]' + u'\u2714' + '[/green bold]' + f' retrieved pages')

    # 4. Get all "pre_scan" id's for each `Page`
    pre_scan_ids = []
    for page in pages:
        # option 1. - get scan ids from `Page` object already in memory
        pre_scan_id = str(page['info']['latest_scan']['id'])
        pre_scan_ids.append(pre_scan_id)

    # 5. Check for all "pre_scan" completion
    print(f'\nchecking pre_scans for each page...')
    wait_for_completion(ids=pre_scan_ids, obj='scan')
    
    # 6. Create new "post_scans" for each `Page`
    print(f'\ncreating post_scans for each page...')
    post_scan_ids = api_scan_site(
        site_id=str(site['id']), 
        api_key=api_key,
        api_root=api_root
    )['data']['ids']
    rprint('[green bold]' + u'\u2714' + '[/green bold]' + f' post_scans created')

    # 7. Check for all "post_scan" completion
    print(f'\nchecking post_scans for each page...')
    wait_for_completion(ids=post_scan_ids, obj='scan', api_root=api_root)

    # 8. Create new `Test` for each `Page`
    pages = api_get_pages(
        site_id=str(site['id']), 
        api_key=api_key,
        api_root=api_root
    )['data']['results']
    test_ids = []
    i = 0
    for page in pages:
        # send the request
        test_id = api_test_page(
            page_id=str(page['id']),
            pre_scan=str(pre_scan_ids[i]),
            post_scan=str(page['info']['latest_scan']['id']),
            api_key=api_key,
            api_root=api_root
        )['data']['ids'][0]
        # record test_id
        test_ids.append(test_id)
        rprint(str(f'\ntesting page {page['page_url']}\
            \n test_id    : {test_id}\
            \n pre_scan   : {pre_scan_ids[i]}\
            \n post_scan  : {page["info"]["latest_scan"]["id"]}'
        ))
        i += 1

    # 9. Check for all `Test` completion
    print(f'\nchecking test completion for each page...')
    wait_for_completion(ids=test_ids, obj='test')

    # decide on client_uri
    client_uri = client_root if client_root else CURSION_CLIENT_BASE_URL

    # checking scores
    success = True
    print('\nTest results:')
    for test_id in test_ids:
        score = api_get_tests(
            test_id=test_id, 
            api_key=api_key,
            api_root=api_root
        )['data']['score']
        _score = str(round(score, 2))
        if score >= threshold:
            rprint(
                ' [green bold]' + u'\u2714' + '[/green bold]' + 
                f' passed {_score}% : {client_uri}/test/{test_id}'
            )
        else:
            rprint(
                ' [red bold]' + u'\u2718' + '[/red bold]' +
                f' failed {_score}% : {client_uri}/test/{test_id}'
            )
            success = False

    # returning results
    return success




def api_run_case(
        site_id: str,
        case_id: str,
        max_wait_time: int=120,
        api_key: str=None,
        api_root: str=None,
        client_root: str=None,
        updates: dict=None,
    ):
    
    """ 
    This method will run a `Case` for the `Site`
    asocaited with the passed id. 

    Steps:
        1. Get requested `Site`
        2. Wait for `Site` to be available
        3. Adjust steps data (from **kwargs)
        4. Initiate the `CaseRun`
        5. Check for `CaseRun` completion
    """

    # 1. get the site
    site = api_get_sites(
        site_id=site_id, 
        api_key=api_key,
        api_root=api_root
    )['data']

    # 2. Wait for `Site` to be available
    wait_time = 0
    site_status = 500
    print(f'checking site availablity...')
    while str(site_status).startswith('5') and wait_time < max_wait_time:
        # sleeping for 5 seconds
        time.sleep(5)
        wait_time += 5
        # check site status
        site_status = requests.get(url=site['site_url']).status_code
    
    # determine if timeout 
    if wait_time >= max_wait_time:
        rprint(
            '[red bold]' + u'\u2718' + '[/red bold]' + 
            ' max wait time reached - proceeding with caution...'
        )
    else:
        rprint(
            '[green bold]' + u'\u2714' + '[/green bold]' 
            + ' site is available'
        )

    # 3. Adjust steps data (from **kwargs)
    print(f'\nadjusting step data...')
    _updates = []
    for i in updates:
        if '-' not in i or ':' not in i:
            rprint(
                '[red bold]' + u'\u2718' + '[/red bold]' + 
                ' step data formatted incorrectly (step-0:value)'
            )
            return

        # parsing data from step
        _str = str(i).split(':')
        value = _str[1]
        index = int(_str[0].split('-')[1])-1

        # adding data to updates
        _updates.append({
            'index': index,
            'value': value
        })

    # done parsing and updating
    rprint('[green bold]' + u'\u2714' + '[/green bold]' + f' step data updated')

    # 4. Create new `CaseRun`
    caserun_data = api_add_caserun(
        case_id=case_id,
        site_id=site_id,
        api_root=api_root,
        updates=_updates
    )

    if not caserun_data['success']:
        rprint(caserun_data)
        return False
    
    # saving caserun_id
    caserun_id = caserun_data['data']['id']

    # 5. Check for `CaseRun` completion
    print(f'\nwaiting for CaseRun completion...')
    wait_for_completion(ids=[caserun_id], obj='caserun', api_root=api_root)
    caserun = api_get_caseruns(
        caserun_id=caserun_id, 
        api_key=api_key,
        api_root=api_root
    )['data']
    passed = True if caserun['status'] == 'passed' else False

    # decide on client_uri
    client_uri = client_root if client_root else CURSION_CLIENT_BASE_URL

    failed = []
    i = 1
    # getting failed steps;
    for step in caserun['steps']:
        if step['action']['status'] == 'failed':
            failed.append(f'Step #{i}, ')
        i += 1

    # displaying results
    print('\nCaseRun results:')
    if passed:
        rprint(
            '[green bold]' + u'\u2714' + '[/green bold]' + 
            f' Passed : {client_uri}/caserun/{caserun_id}' 
        )
    else:
        rprint(
            f'{"\n[red bold]" + u"\u2718" + "[/red bold]"}' + 
            f' Failed : {client_uri}/caserun/{caserun_id}' + 
            f'\n failed steps : {[n for n in failed]}'
        )

    # returning results
    return passed




def api_run_flow(
        site_id: str,
        flow_id: str,
        max_wait_time: int=240,
        api_key: str=None,
        api_root: str=None,
        client_root: str=None
    ):
    
    """ 
    This method will run a `Flow` for the `Site`
    asocaited with the passed id. 

    Steps:
        1. Get requested `Site`
        2. Wait for `Site` to be available
        3. Initiate the `FlowRun`
        4. Check for `FlowRun` completion
    """

    # 1. get the site
    site = api_get_sites(
        site_id=site_id, 
        api_key=api_key,
        api_root=api_root
    )['data']

    # 2. Wait for `Site` to be available
    wait_time = 0
    site_status = 500
    print(f'checking site availablity...')
    while str(site_status).startswith('5') and wait_time < max_wait_time:
        # sleeping for 5 seconds
        time.sleep(5)
        wait_time += 5
        # check site status
        site_status = requests.get(url=site['site_url']).status_code
    
    # determine if timeout 
    if wait_time >= max_wait_time:
        rprint(
            '[red bold]' + u'\u2718' + '[/red bold]' + 
            ' max wait time reached - proceeding with caution...'
        )
    else:
        rprint(
            '[green bold]' + u'\u2714' + '[/green bold]' 
            + ' site is available'
        )

    # 3. Create new `FlowRun`
    print(f'\nstarting new FlowRun')
    flowrun_data = api_add_flowrun(
        flow_id=flow_id,
        site_id=site_id,
        api_root=api_root
    )

    if not flowrun_data['success']:
        rprint(flowrun_data)
        return False
    
    # saving flowrun_id
    flowrun_id = flowrun_data['data']['id']

    # 4. Check for `FlowRun` completion
    print(f'\nwaiting for FlowRun completion...')
    wait_for_completion(ids=[flowrun_id], obj='flowrun', api_root=api_root)
    flowrun = api_get_flowruns(
        flowrun_id=flowrun_id, 
        api_key=api_key, 
        api_root=api_root
    )['data']
    passed = True if flowrun['status'] == 'passed' else False

    # decide on client_uri
    client_uri = client_root if client_root else CURSION_CLIENT_BASE_URL

    failed = []
    i = 1
    # getting failed jobs;
    for job in flowrun['nodes']:
        if job['data']['status'] == 'failed':
            failed.append(f'Job #{job['data']['id']} ({job['data']['task_type']}), ')
        i += 1

    # displaying results
    print('\nFlowRun results:')
    if passed:
        rprint(
            ' [green bold]' + u'\u2714' + '[/green bold]' + 
            f' Passed : {client_uri}/flowrun/{flowrun_id}' 
        )
    else:
        rprint(
            ' [red bold]' + u'\u2718' + '[/red bold]' + 
            f' Failed : {client_uri}/flowrun/{flowrun_id}' + 
            f'\n failed jobs : {[n for n in failed]}'
        )

    # returning results
    return passed








