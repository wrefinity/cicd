ssh -i "cicd_kene.pem" ubuntu@ec2-52-14-201-82.us-east-2.compute.amazonaws.com


name:  deployment to EC2

on:
  push:
    branches: ["main"]

jobs:
  build:
    runs-on: self-hosted
    steps:
      - name: checkout code 
        uses: actions/checkout@v2
      - name: get the enviromental variables
        run: echo "PORT=${{secrets.PORT}}" >> .env
      - name: login to docker hub
        env:
          username: ${{secrets.DOCKER_USER}}
          password: ${{secrets.DOCKER_PASSWORD}}
        run: |
          echo $username
          docker login -u $username -p $password
      - name: build image
        run: sudo docker build -t ${{secrets.DOCKER_USER}}/fasty .
      - name: push image
        run: sudo docker push ${{secrets.DOCKER_USER}}/fasty:latest
       
     
  deploy:
    needs: build
    runs-on: self-hosted
    steps:
      - name: pull the image from docker-hub 
        run: sudo docker pull wrashtech/fasty:latest
      - name: delete old fasty container
        run: sudo docker rm -f wrashtech/fasty
      - name: run new container
        run: sudo docker run -d -p 8000:8000 --name wrashtech/fasty wrashtech/fasty
      
