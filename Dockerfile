# base image
# a little overkill to do full ubuntu base
FROM ubuntu:20.04

# set TZ since can't interact during setup
ENV TZ=America/Los_Angeles \
    DEBIAN_FRONTEND=noninteractive

# ubuntu installing - python, pip, nano
RUN apt-get update &&\
    apt-get install python3.9 -y &&\
    apt-get install python3-pip -y

# exposing default port for streamlit
EXPOSE 8501

# making directory of app
WORKDIR /fitness-tracker-streamlit

# copy over requirements
COPY requirements.txt ./requirements.txt

# install pip then packages
RUN pip3 install -r requirements.txt

# copying all files over
COPY . .

# cmd to launch app when container is run
CMD streamlit run app.py

# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'

RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'
