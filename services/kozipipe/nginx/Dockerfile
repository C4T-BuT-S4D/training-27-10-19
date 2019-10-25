FROM nginx:1.15.9-alpine

ADD ./conf/ /etc/nginx/conf.d/
ADD ./proxy_params /etc/nginx/proxy_params

CMD ["nginx", "-g", "daemon off;"]