FROM python:3.8-slim-buster

# ==================== Environment ===================== #
ENV SAVE_FOLDER='/thoughtinator/save'

# ====================== Installs ====================== #
RUN apt-get update

# -------------= NPM =-------------- #
RUN apt-get install -y npm
RUN npm install -g npm@latest

# -----------= Python =------------- #
ADD requirements.txt /requirements.txt
RUN pip3.8 install -r /requirements.txt

# Port Exposing 8080: GUI, 5000: API, 8000: Upload
EXPOSE 8080 5000 8000

# Wait For It setup
ADD scripts/wait-for-it.sh /wait-for-it.sh
RUN chmod 755 wait-for-it.sh

# Build GUI
WORKDIR /thoughtinator/gui/react/thoughtinator-gui
RUN npm install
RUN npm install react react-dom react-datepicker bootstrap
RUN npm run build

WORKDIR /