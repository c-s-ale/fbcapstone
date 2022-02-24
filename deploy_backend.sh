echo "Deploying Backend"
cd backend
sudo aws ecr-public get-login-password --region us-east-1 | sudo docker login --username AWS --password-stdin public.ecr.aws/v9v8o7t4
sudo docker build -t s2t-backend .
sudo docker tag s2t-backend:latest public.ecr.aws/v9v8o7t4/s2t-backend:latest
sudo docker push public.ecr.aws/v9v8o7t4/s2t-backend:latest
cd ..
cd aws_deploy
eb deploy