FROM python:3.12.4-alpine3.20

WORKDIR /app
COPY . /app

EXPOSE 8000

# https://gitlab.alpinelinux.org/alpine/aports/-/issues/12057
ENV TZ="America/Caracas"
RUN apk add --no-cache tzdata
RUN ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime

# Install Node.js and npm
RUN apk add --no-cache nodejs npm
# Install psql client
RUN apk add --no-cache postgresql-client

# Install Python dependencies
RUN pip install -r requirements.txt --no-cache-dir

RUN npm install
RUN npm run build

CMD ["python", "app.py"]
