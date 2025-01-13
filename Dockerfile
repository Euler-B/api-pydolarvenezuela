# node image is used to build the frontend
FROM node:23-alpine3.20 AS build

WORKDIR /app
COPY . /app

RUN npm install
RUN npm run build

# python image is used to run the backend
FROM python:3.12.4-alpine3.20

WORKDIR /app
COPY --from=build /app /app

EXPOSE 8000

# https://gitlab.alpinelinux.org/alpine/aports/-/issues/12057
ENV TZ="America/Caracas"
RUN apk add --no-cache tzdata
RUN ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime

# Install psql client
RUN apk add --no-cache postgresql-client

# Install Python dependencies
RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "app.py"]
