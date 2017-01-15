FROM python:2.7-alpine
# FROM python:2.7-slim


ADD ./app.py /app.py
ADD ./run.sh /run.sh
ADD etc/resolv.conf /etc/resolv.conf
ADD ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt && \
    chmod +x /run.sh

EXPOSE 5000
CMD ["/run.sh"]
