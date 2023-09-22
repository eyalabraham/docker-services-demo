#!/bin/bash
#
# Usage: ./ocpdeploy.sh <namespace> <storage_class>
# Example: ./ocpdeploy.sh library-ns ocs-storagecluster-cephfs
#

set -x
NAMESPACE=$1
SC_NAME=$2

oc new-project $NAMESPACE

cat docker-demo-pvc.yaml | sed s/your-storage-class-name/$SC_NAME/ > docker-demo-pvc-tmp.yaml
cat frontend-route.yaml | sed s/NAMESPACE/$NAMESPACE/ > frontend-route-tmp.yaml

oc create -f docker-demo-pvc-tmp.yaml -n $NAMESPACE
oc create -f sqlbackend-deployment.yaml -n $NAMESPACE
oc create -f sqlbackend-service.yaml -n $NAMESPACE
oc create -f patronsdb-deployment.yaml -n $NAMESPACE
oc create -f patrons-rest-service.yaml -n $NAMESPACE
oc create -f borrowingdb-deployment.yaml -n $NAMESPACE
oc create -f borrowing-rest-service.yaml -n $NAMESPACE
oc create -f catalogdb-deployment.yaml -n $NAMESPACE
oc create -f catalog-rest-service.yaml -n $NAMESPACE
oc create -f liblogic-deployment.yaml -n $NAMESPACE
oc create -f liblogic-rest-service.yaml -n $NAMESPACE
oc create -f frontend-deployment.yaml -n $NAMESPACE
oc create -f frontend-service.yaml -n $NAMESPACE
oc create -f frontend-route-tmp.yaml -n $NAMESPACE

# Cleanup
rm docker-demo-pvc-tmp.yaml
rm frontend-route-tmp.yaml