# k8s-reload
Custom Kubernetes Controller to reload pods automatically if configmaps are changed/ updated. 🔄 

- [k8s-reload](#k8s-reload)
  - [Quickstart](#quickstart)
    - [Instal contoller via helm chart:](#instal-contoller-via-helm-chart)
    - [Build k8s-reload controller image:](#build-k8s-reload-controller-image)
    - [Run a demo application to test controller's functionality:](#run-a-demo-application-to-test-controllers-functionality)
  - [Usecases](#usecases)
## Quickstart

### Instal contoller via helm chart:

    ## Clone the repository.
    git clone https://github.com/shivanshthapliyal/k8s-reload.git
    cd k8s-reload/chart

    ## Install Helm chart
    helm upgrade --install k8s-reload-controller-helm . -f values.yaml


### Build k8s-reload controller image:

    cd controller
    docker build -t k8s-reload:1.0 -f k8s-reload-controller.dockerfile . --no-cache

### Run a demo application to test controller's functionality:

    cd demo-manifests
    docker build -t demo-frontend-app:1.0 -f demo-frontend-app.dockerfile . --no-cache
    kubectl apply -f demo-deployment.yaml demo-configmap.yaml

Now, try modifying the configmap and see the controller automatically recreate the pods!

    $ k logs -f k8s-reload-controller-helm-5d9cb7bb74-kzcgl k8s-reload-controller
    2022-04-11 17:33:10,638 Starting the service
    2022-04-11 17:33:30,145 Modification detected on configmap - with label
    2022-04-11 17:33:30,194 demo-frontend-app-b75647989-4g5vs was deleted successfully


## Usecases
One usecase is while using [secrets-store-csi-driver-provider-aws](https://github.com/aws/secrets-store-csi-driver-provider-aws), when you change the parameter or secret in Parameter Store or Secret Manager, the configmap changes in the env but the pods/ deployments don't reload on their own and need to be deleted manually.    
