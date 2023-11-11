# Build stage
FROM node:14 AS build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:stable-alpine
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage ../static/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]