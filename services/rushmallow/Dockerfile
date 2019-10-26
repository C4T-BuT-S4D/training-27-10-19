FROM mcr.microsoft.com/dotnet/core/sdk:2.2 

MAINTAINER @keltecc

ADD Rushmallow /var/task

WORKDIR /var/task/Rushmallow

RUN dotnet publish -c Release -o service

ENTRYPOINT ["dotnet", "service/Rushmallow.dll"]
