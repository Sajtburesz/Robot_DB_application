FROM node:14 as build-stage

WORKDIR /frontend

COPY package*.json /frontend/

RUN npm install

COPY . /frontend/

RUN npm run build

FROM nginx:stable as production-stage

COPY --from=build-stage /frontend/dist /usr/share/nginx/html
COPY --from=build-stage /frontend/templates/index.html /usr/share/nginx/html/index.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
