import requests
import os
import json
import logging
import sys

log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)

base_url = "http://127.0.0.1:8001"

namespace = os.getenv("res_namespace", "default")

def kill_pods(label):
    url = "{}/api/v1/namespaces/{}/pods?labelSelector={}".format(
        base_url, namespace, label)
    r = requests.get(url)
    response = r.json()
    pods = [p['metadata']['name'] for p in response['items']]
    for p in pods:
        url = "{}/api/v1/namespaces/{}/pods/{}".format(base_url, namespace, p)
        r = requests.delete(url)
        if r.status_code == 200:
            log.info("{} was deleted successfully".format(p))
        else:
            log.error("Could not delete {}".format(p))

def event_loop():
    log.info("Starting k8s-reload controller")
    url = '{}/api/v1/namespaces/{}/configmaps?watch=true"'.format(
        base_url, namespace)
    r = requests.get(url, stream=True)
    for line in r.iter_lines():
        try:
            obj = json.loads(line)
            event_type = obj['type']
            configmap_name = obj["object"]["metadata"]["name"]
            if "annotations" in obj["object"]["metadata"]:
                if "k8s-reload/podDeleteMatch" in obj["object"]["metadata"]['annotations']:
                    label = obj["object"]["metadata"]["annotations"]["k8s-reload/podDeleteMatch"]
            if event_type == "MODIFIED":
                log.info(f"Modification detected on configmap - with label k8s-reload/podDeleteMatch={label}")
                kill_pods(label)
        except:
            log.info("No EventType")

event_loop()