# network-logger
Python app to debug networking issues between pod to pod communication 

1. Clone `network-logger`
```bash
$ git clone https://github.com/stakater/network-logger.git
$ cd network-logger/
```

2. Create new project by name `network-logger-pod-b` and install Pod-B's manifest
```bash
network-logger$ oc new-project network-logger-pod-b

network-logger$ oc create -f manifests/pod-b
deployment.apps/pod-b-app created
service/pod-b-service created

network-logger$ oc get po
NAME                         READY     STATUS    RESTARTS   AGE
pod-b-app-7dccfcc5c9-j55zx   1/1       Running   0          43s

network-logger$ oc get svc
NAME            TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
pod-b-service   NodePort   172.30.114.49   <none>        6000:31918/TCP   91s
```

3. Generating the route for Pod-B
- note: Replace labels `-l pod=pod-b,provider=stakater,router=default` as per your environment 
```bash
network-logger$ oc expose service pod-b-service -l pod=pod-b,provider=stakater,router=default --name=pod-b-route
route.route.openshift.io/pod-b-route exposed

network-logger$ oc get routes
NAME          HOST/PORT                                                                  PATH      SERVICES        PORT      TERMINATION   WILDCARD
pod-b-route   pod-b-route-network-logger-pod-b.apps.binero-test.8sdzwd1l.kubeapp.cloud             pod-b-service   http                    None

network-logger$ curl pod-b-route-network-logger-pod-b.apps.binero-test.8sdzwd1l.kubeapp.cloud/pod/b?test=1
{"response":{"test":"1"},"source":"POD-B"}

```

4. Update `POD_B_ROUTE` env in `pod-a`'s deployment env with `pod-b-route` generated above.
```yaml
        name: pod-a-app
        env:
          - name: APP_PORT
            value: "5000"
          - name: POD_B_ROUTE
            value:
```
To
```yaml
        name: pod-a-app
        env:
          - name: APP_PORT
            value: "5000"
          - name: POD_B_ROUTE
            value: pod-b-route-network-logger-pod-b.apps.binero-test.8sdzwd1l.kubeapp.cloud
```

5. Create new project by name `network-logger-pod-a` and install Pod-A's manifest
```bash
network-logger$ oc new-project network-logger-pod-a

network-logger$ oc create -f manifests/pod-a
deployment.apps/pod-a-app created
service/pod-a-service created

network-logger$ oc get po
NAME                         READY     STATUS    RESTARTS   AGE
pod-a-app-548c7bfbc7-5b5cs   1/1       Running   0          6s

network-logger$ oc get svc
NAME            TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
pod-a-service   NodePort   172.30.10.63   <none>        5000:30556/TCP   13s
```

6. Generating the route for Pod-A
- note: Replace labels `-l pod=pod-a,provider=stakater,router=default` as per your environment 
```bash
network-logger$ oc expose service pod-a-service -l pod=pod-a,provider=stakater,router=default --name=pod-a-route
route.route.openshift.io/pod-a-route exposed

network-logger$ oc get routes
NAME          HOST/PORT                                                                  PATH      SERVICES        PORT      TERMINATION   WILDCARD
pod-a-route   pod-a-route-network-logger-pod-a.apps.binero-test.8sdzwd1l.kubeapp.cloud             pod-a-service   http                    None

network-logger$ curl pod-a-route-network-logger-pod-a.apps.binero-test.8sdzwd1l.kubeapp.cloud/pod/a?test=2
{"response":{"response":{"test":"2"},"source":"POD-B"},"source":"POD-A"}

```