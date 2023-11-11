# Build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
ENV NODE_ENV production
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /static/dist /static/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
