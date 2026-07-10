### This app was tested on k8s from DigitalOcean. The StorageClass for the Postgres uses the do class.
<ins></ins>

1. Build an image, and push it to the registory

&nbsp;&nbsp;&nbsp;&nbsp;docker build -t stateful-flask:v0 -f task/Dockerfile <context here>  
&nbsp;&nbsp;&nbsp;&nbsp;docker login  
&nbsp;&nbsp;&nbsp;&nbsp;docker tag stateful-flask:v0 <dockerhub account>/stateful-flask:v0  
&nbsp;&nbsp;&nbsp;&nbsp;docker push <dockerhub account>/stateful-flask:v0  

2. Deploy postgres to k8s 

&nbsp;&nbsp;&nbsp;&nbsp;kubectl apply -f kubernetes/*.yaml  

3. Deploy web app to kubernetes  

&nbsp;&nbsp;&nbsp;&nbsp;kubectl create -n statefull-webapp  
&nbsp;&nbsp;&nbsp;&nbsp;pod=$(kubectl get pod -n stateful-flask -l app=stateful-flask -o jsonpath='{.items[0].metadata.name}')  

&nbsp;&nbsp;&nbsp;&nbsp;kubectl exec -it $pod -n stateful-flask -- flask db init  
&nbsp;&nbsp;&nbsp;&nbsp;kubectl exec -it $pod -n stateful-flask -- flask db migrate  
&nbsp;&nbsp;&nbsp;&nbsp;kubectl exec -it $pod -n stateful-flask -- flask db upgrade  

4. Install ingress  

&nbsp;&nbsp;&nbsp;&nbsp;curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4  
&nbsp;&nbsp;&nbsp;&nbsp;chmod 700 get_helm.sh  
&nbsp;&nbsp;&nbsp;&nbsp;./get_helm.sh  

&nbsp;&nbsp;&nbsp;&nbsp;helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx  
&nbsp;&nbsp;&nbsp;&nbsp;helm repo update  
&nbsp;&nbsp;&nbsp;&nbsp;helm install nginx-ingress ingress-nginx/ingress-nginx --set controller.publishService.enabled=true --create-namespace  --namespace ingress-nginx  

5. Test

&nbsp;&nbsp;&nbsp;&nbsp;curl -X POST -H "Content-Type: application/json" -d '{"title": "Learn Flask", "description": "First task"}' http://<website name here>/tasks  
