FROM node:latest as build-stage
WORKDIR /vuejs
COPY package*.json ./
RUN npm install
COPY ./ .
RUN npm run build
COPY ../templates/index.html ./dist/index.html

FROM nginx as production-stage
RUN mkdir /vuejs
COPY --from=build-stage /vuejs/dist /vuejs
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf