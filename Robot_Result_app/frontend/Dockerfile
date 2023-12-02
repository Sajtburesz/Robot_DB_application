FROM node:14 as build-stage

WORKDIR /frontend

COPY package*.json /frontend/

RUN npm install

COPY . /frontend/

RUN npm run build

FROM nginx:stable as production-stage

COPY --from=build-stage /frontend/dist /usr/share/nginx/html
COPY --from=build-stage /frontend/templates/index.html /usr/share/nginx/html/index.html

COPY ./nginx.conf.template /etc/nginx/conf.d/

EXPOSE 80

CMD /bin/bash -c "export NGINX_HOST=$NGINX_HOST && export BACKEND_PORT=$BACKEND_PORT && envsubst '\$NGINX_HOST \$BACKEND_PORT' < /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"



