#!/usr/bin/python

import yaml
import sys
import json


def fixUpConfigs(clusterEnv):
    with open("control-tower-cluster.yaml") as f_cluster, open("config.yaml") as f_config:
        # load the files as yamls
        cluster = yaml.safe_load(f_cluster)
        config = yaml.safe_load(f_config)

        fullClusterName = clusterEnv + "-" + config['clusterName']

        # change configurations
        cluster['metadata']['name'] = fullClusterName
        cluster['metadata']['region'] = config['clusterRegion']
        cluster['metadata']['version'] = str(config['clusterVersion'])
        cluster['managedNodeGroups'][0]['desiredCapacity'] = config['desiredCapacity']
        cluster['managedNodeGroups'][0]['maxSize'] = config['maxSize']
        cluster['managedNodeGroups'][0]['minSize'] = config['minSize']
        cluster['managedNodeGroups'][0]['labels']['alpha.eksctl.io/cluster-name'] = fullClusterName

        # fix up the subnets
        subnets = {"private": {}}
        for i, subnet in enumerate(config['subnets'].split(",")):
            subnets["private"]["subnet-" +
                               str(i)] = {"az": "subnet-" + str(i), "id": subnet.strip()}
            # subnets["private"]["subnet" ]["id"] = subnet
        cluster['vpc']['subnets'] = subnets
        # print(subnets)
        print(yaml.dump(cluster, default_flow_style=False, sort_keys=False))
        # sys.exit(0)


def getClusters():
    with open("config.yaml") as f_config:
        # load the files as yamls
        config = yaml.safe_load(f_config)
        json.dump(config["clusters"], sys.stdout)


def fixKubernetesYamls(image, repoName, branchName):
    with open("infra/app/deployment.yaml") as f_deployment:
        deployment = yaml.safe_load(f_deployment)
        print(deployment["metadata"])
        deployment["metadata"] = {
            "name": repoName,
            "namespace": branchName,
            "labels": {"app": repoName}
        }
        deployment["spec"]["selector"] = {"matchLabels": {"app": repoName}}

        deployment["spec"]["template"]["spec"]["containers"][0]["name"] = repoName
        deployment["spec"]["template"]["spec"]["containers"][0]["image"] = image
        print(yaml.dump(deployment, default_flow_style=False, sort_keys=False))
