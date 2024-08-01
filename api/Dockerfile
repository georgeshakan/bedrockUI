# 
FROM  python:3.12
#
RUN apt update 

RUN apt install awscli -y

RUN apt install python3-pip -y



#
RUN apt-get install poppler-utils -y
# 
WORKDIR /code

# 
COPY ./requirements.txt ./requirements.txt

#
RUN pip install --upgrade pip

# 
RUN pip install --no-cache-dir -r ./requirements.txt

#


# 
COPY ./ ./

#CMD ["python3", "scrap.py"]


CMD ["streamlit", "run", "app.py"]    