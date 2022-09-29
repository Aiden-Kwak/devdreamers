FROM python:3.9.0

RUN mkdir /root/.ssh/

ADD ./.ssh/id_rsa /root/.ssh/id_rsa

RUN chmod 600 /root/.ssh/id_rsa

RUN touch /root/.ssh/known_hosts

RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

WORKDIR /home/

RUN echo "testing"

RUN git clone git@github.com:Dreaming-Developer/deploy.git

WORKDIR /home/deploy/

RUN pip install --upgrade pip

RUN pip install -r deploy/requirements.txt

RUN pip install gunicorn

EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --noinput --settings=website.settings.deploy && python manage.py migrate --settings=website.settings.deploy && gunicorn website.wsgi --env DJANGO_SETTINGS_MODULE=website.settings.deploy --bind 0.0.0.0:8000"]
