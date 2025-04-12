FROM node:20-alpine

WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
RUN apk add --no-cache curl && curl -1sLf 'https://artifacts-cli.infisical.com/setup.deb.sh' | sh && apk add --no-cache infisical
COPY . .
RUN chmod +x run.sh

EXPOSE 3000
