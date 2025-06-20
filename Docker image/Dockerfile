FROM python:3.11-bookworm

ARG CASE=1

RUN wget https://ccl.northwestern.edu/netlogo/6.3.0/NetLogo-6.3.0-64.tgz
RUN tar zxvf NetLogo-6.3.0-64.tgz
RUN mv ./NetLogo\ 6.3.0 /opt/netlogo
RUN rm NetLogo-6.3.0-64.tgz
ENV NETLOGO_HOME=/opt/netlogo
ENV PATH=$NETLOGO_HOME:$PATH
RUN chmod -R 777 /opt/netlogo
ADD files/src /root/experiments/case1
ADD files/src /root/experiments/case2
ADD files/requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt
RUN apt update
RUN apt install texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended dvipng cm-super -y
COPY files/case1.ini /root/experiments/case1/params.ini
COPY files/case2.ini /root/experiments/case2/params.ini
ENV CASE_DIR=/root/experiments/case${CASE}
WORKDIR $CASE_DIR
VOLUME /root/experiments
ENTRYPOINT ["python3", "toolkit_lib.py"]
