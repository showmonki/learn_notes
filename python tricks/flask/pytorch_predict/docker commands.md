Refs:
- https://cloud.tencent.com/developer/article/1500255?from=15425
- https://pytorch.org/tutorials/intermediate/flask_rest_api_tutorial.html
- https://github.com/avinassh/pytorch-flask-api

Step 1: build docker image
```
docker build -t docker-flask-pytorch:0.1 .
```

Step 2: run docker
```
# run command 1 - attach&debug:
docker run --name flask_app_pytorch -v $PWD/app:/app -p 5000:5000 docker-flask-pytorch:0.1
# run command 2 run&product:
docker run -d --name flask_app_pytorch --restart=always -p 8091:80 docker-flask-pytorch:0.1
```


Other:
该镜像包含python、ngix、uwsgi完整环境，只需要在部署时指定端口映射便可以自动部署应用。要停止并删除此容器，请运行下面命令：
```
docker stop flaskapp && docker rm flaskapp
```

此外，如果我们仍然需要上面调试功能或修改部分代码，也可以像上面一样以调试模式运行容器:
```
docker run -it --name flaskapp -p 5000:5000 -v $PWD/app:/app docker-flask:0.1 -d debug
```

