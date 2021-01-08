from flask import Flask, make_response

import os
import json
import urllib.request
import time


app = Flask(__name__)


def generateMetrics():
    
    #get env vars
    url=str(os.environ["ENV_URL"])
    password=str(os.environ["ENV_PASSWORD"])


    # Make sure we got the trailing slash at the URL
    if str.endswith(url, "/"):
        fetch_url = url + "stat?password=" + urllib.parse.quote_plus(password)
    else:
        fetch_url = url + "/stat?password=" + urllib.parse.quote_plus(password)

    try:
    	resp = urllib.request.urlopen(fetch_url)
    except Exception:
        print("Could not send GET request to given URL. Check url parameter!")
        exit(1)
    # Authorization failed
    if resp.code == 403:
        print("Authorization with rspamd web interface failed. Check password parameter!")
        exit(1)

    elif resp.code == 404:
        print("HTTP server returned HTTP status code 404. Check url parameter!")
        exit(1)

    elif resp.code == 200:
        print("all right")
        # Successful call
    else:
        print("Web request returned unhandled HTTP status code " + str(resp.code) + ". Please open an issue at GitHub "
                                                                                "with further details.")
        exit(1)

    import json
    json = json.loads(resp.read().decode('utf-8'))

    action_reject = str(json["actions"]["reject"])
    action_soft_reject = str(json["actions"]["soft reject"])
    action_rewrite = str(json["actions"]["rewrite subject"])
    action_add_header = str(json["actions"]["add header"])
    action_greylist = str(json["actions"]["greylist"])
    action_no_action = str(json["actions"]["no action"])

    stat_scanned = str(json["scanned"])
    stat_learned = str(json["learned"])
    stat_spam_count = str(json["spam_count"])
    stat_ham_count = str(json["ham_count"])
    stat_connections = str(json["connections"])
    stat_control_connections = str(json["control_connections"])
    stat_pools_allocated = str(json["pools_allocated"])
    stat_pools_freed = str(json["pools_freed"])
    stat_bytes_allocated = str(json["bytes_allocated"])
    stat_chunks_allocated = str(json["chunks_allocated"])
    stat_chunks_freed = str(json["chunks_freed"])
    stat_chunks_oversized = str(json["chunks_oversized"])
    stat_fragmented = str(json["fragmented"])
    stat_total_learns = str(json["total_learns"])
    stat_fuzzy_rspamd = str(json["fuzzy_hashes"]["rspamd.com"])


    RETURN_VALUES="""
rspamd_actions_reject {0}
rspamd_actions_soft_reject {1}
rspamd_actions_rewrite_subject {2}
rspamd_actions_add_header {3}
rspamd_actions_greylist {4}
rspamd_actions_no_action {5}
rspamd_stats_scanned {6}
rspamd_stats_learned {7}
rspamd_stats_spam_count {8}
rspamd_stats_ham_count {9}
rspamd_stats_connections {10}
rspamd_stats_control_connections {11}
rspamd_stats_pools_allocated {12}
rspamd_stats_pools_freed {13}
rspamd_stats_bytes_allocated {14}
rspamd_stats_chunks_allocated {15}
rspamd_stats_chunks_freed {16}
rspamd_stats_chunks_oversized {17}
rspamd_stats_fragmented {18}
rspamd_stats_total_learns {19}
rspamd_stats_fuzzy {20}
    """.format(
        action_reject, 
        action_soft_reject, 
        action_rewrite, 
        action_add_header, 
        action_greylist, 
        action_no_action,
        stat_scanned, 
        stat_learned,
        stat_spam_count,
        stat_ham_count,
        stat_connections,
        stat_control_connections,
        stat_pools_allocated,
        stat_pools_freed,
        stat_bytes_allocated,
        stat_chunks_allocated,
        stat_chunks_freed,
        stat_chunks_oversized,
        stat_fragmented,
        stat_total_learns,
        stat_fuzzy_rspamd)

    print(RETURN_VALUES)
    return RETURN_VALUES



@app.route('/metrics2')
def metrics2():
    response = make_response(generateMetrics(), 200)
    response.mimetype = "text/plain"
    return response


@app.route('/metrics')
def metrics():
    return generateMetrics()



if __name__ == '__main__':
    app.run(host='0.0.0.0',port="5000")