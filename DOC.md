# HelloFresh DevOps Test \
Test link: \
*https://github.com/hellofreshdevtests/pathfinder177-devops-test*

Node with running api and corresponding endpoints: \
*http://minikube-108073090.eu-central-1.elb.amazonaws.com* \
NB I hope AWS allows me to use free tier until you test it =)


## Code
1. python as programming language: it is quick to debug because of interpretation nature and i do not know GO yet but looking forward to.
2. flask: small and power enough to attain the goals. Each endpoint uses their own blueprint thus i implemented separation of concerns.
3. sqlite: it does not demand to be deployed as statefulset and be used because of time economy and json handling capabilities.

## Infrastructure
1. aws: the most comprehensive documented cloud and they do not demand a card because my was rejected by many clouds providers
2. k8s: implemented as minikube
3. docker: the most popular and understandable runtime although k8s goes without it further

## Approximate scheme of request's flow
Request(http) -> AWS Load Balancer:80 -> AWS Target Group -> AWS Node:32080 \
    -> AWS Node Network Interface -> IPTables chains of rules  -> Container network Interface:8080 -> \
    -> ~corresponding endpoint(just an abstraction) -> data requested by cursor from db -> response assembling -> response returning in reverse order

## TODO:
1) Tests should work
2) Database should be on a volume to make app stateful
3) *Discuss my desicion deeply if you think that it is a decent one