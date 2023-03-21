import urllib.request
from flask import Flask
from flask import jsonify
import json
from kafka import KafkaConsumer

# Required for Kubernetes POD Management, ensure RBAC authorisation is configured
import os
import pint
import kubernetes
from kubernetes import client, config, watch
from kubernetes.client.models import V1PodSpec
from kubernetes.client.models import V1Container
from kubernetes.client.models import V1Pod
from kubernetes.client.models import V1ObjectMeta


consumer = KafkaConsumer('my-topic', bootstrap_servers=['34.28.118.32:9094'], auto_offset_reset='latest')

i=0
for message in consumer:
    message_1 = message.value
    print(message_1)
    my_json = message_1.decode('utf8')
    print(my_json)

    
    
    
    #'''
    
    config.load_incluster_config()
    v1 = kubernetes.client.CoreV1Api()

    container_name = 'data-flowcontainer'
    namespace = 'default'
    pod_name = 'my-dataflow-pod'

    while True:
        resp = v1.read_namespaced_pod(name=pod_name, namespace='default')
        if resp.status.phase == 'Succeeded':
            break

    delete_response = v1.delete_namespaced_pod(name=pod_name, namespace=namespace)

    image = 'gcr.io/mimetic-parity-378803/dataflow_pipeline:latest'
    container = V1Container(name=container_name, image=image)
    podspec = V1PodSpec(containers=[container], restart_policy="Never")
    metadata = V1ObjectMeta(name=pod_name, namespace=namespace)
    pod = V1Pod(api_version='v1', kind='Pod', metadata=metadata, spec=podspec)

    my_pod = v1.create_namespaced_pod(namespace, pod)

    while True:
        resp = v1.read_namespaced_pod(name=pod_name, namespace='default')
        if resp.status.phase != 'Pending':
            break
        time.sleep(1)

    #ret = v1.read_namespaced_pod(pod_name, namespace)

    #if ret:
        #details = "POD Created"

    #print(jsonify({"message": "POD Details ", "Information: ": details}))


    #'''
consumer.close()
