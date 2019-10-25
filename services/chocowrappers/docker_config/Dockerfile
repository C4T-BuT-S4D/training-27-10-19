FROM mcr.microsoft.com/dotnet/core/aspnet:2.2

ADD ./src /app
ADD ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]