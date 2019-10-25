FROM mcr.microsoft.com/dotnet/core/sdk:2.2

ADD ./build_entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ADD . /app

CMD ["/entrypoint.sh"]