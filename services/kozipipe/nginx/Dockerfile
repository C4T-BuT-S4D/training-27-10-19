FROM nginx:1.15.9-alpine

RUN rm -f /etc/nginx/conf.d/default.conf

ADD ./conf/ /etc/nginx/conf.d/
ADD ./proxy_params /etc/nginx/proxy_params

CMD ["nginx", "-g", "daemon off;"]
