FROM python:3
WORKDIR /app/
COPY src /app/
RUN pip install ply -i https://pypi.tuna.tsinghua.edu.cn/simple