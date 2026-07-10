### This app can work in k8s deployed to DigitalOcean. The StorageClass for postgres is using DO class.

1. Build an image, and push it to the registory

&nbsp;&nbsp;&nbsp;&nbsp;docker build -t stateful-flask:v0 -f task/Dockerfile <context here>  
&nbsp;&nbsp;&nbsp;&nbsp;docker login  
&nbsp;&nbsp;&nbsp;&nbsp;docker tag stateful-flask:v0 <dockerhub account>/stateful-flask:v0  
&nbsp;&nbsp;&nbsp;&nbsp;docker push <dockerhub account>/stateful-flask:v0  

2. Deploy postgres to k8s 

kubectl apply -f kubernetes/*.yaml  

3. Deploy web app to kubernetes  

kubectl create -n statefull-webapp  
pod=$(kubectl get pod -n stateful-flask -l app=stateful-flask -o jsonpath='{.items[0].metadata.name}')  

kubectl exec -it $pod -n stateful-flask -- flask db init  
kubectl exec -it $pod -n stateful-flask -- flask db migrate  
kubectl exec -it $pod -n stateful-flask -- flask db upgrade  

4. Install ingress  

curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4  
chmod 700 get_helm.sh  
./get_helm.sh  

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx  
helm repo update  
helm install nginx-ingress ingress-nginx/ingress-nginx --set controller.publishService.enabled=true --create-namespace  --namespace ingress-nginx  

5. Test

curl -X POST -H "Content-Type: application/json" -d '{"title": "Learn Flask", "description": "First task"}' http://<website name here>/tasks  
