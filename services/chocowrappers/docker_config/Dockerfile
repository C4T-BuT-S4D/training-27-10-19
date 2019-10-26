FROM mcr.microsoft.com/dotnet/core/aspnet:2.2

MAINTAINER @pomo_mondreganto

ADD ./src /app
ADD ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]