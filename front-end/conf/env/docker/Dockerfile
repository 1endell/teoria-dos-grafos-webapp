# Etapa 1: build da aplicação
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Etapa 2: servir arquivos com Nginx
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

# Remove o arquivo default do nginx e adiciona o nosso
RUN rm /etc/nginx/conf.d/default.conf
COPY conf/env/nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
