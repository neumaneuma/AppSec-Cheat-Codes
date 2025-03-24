FROM node:22.14.0-slim

WORKDIR /frontend

EXPOSE 12300

COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm install

COPY . .
