unit session;

uses System.Net;
uses System.Security.Cryptography;
uses System.Text;
uses crypto;
var
	secret: string;

procedure LoginSession(user: string; var ctx: System.Net.HttpListenerContext);
begin
	ctx.Response.AppendCookie(new System.Net.Cookie('session', user + ':' + Createmd5(user + secret)));
end;

function GetUserSession(var ctx: System.Net.HttpListenerContext): string;
var
	sessionCookie: string;
	c: 	System.Net.Cookie;
begin
	foreach c in ctx.Request.Cookies do begin
		if (c.Name = 'session') then sessionCookie := c.Value;
	end;
	var parts := sessionCookie.Split(':');
	if ((Length(parts) = 2) and (Createmd5(parts[0] + secret) = parts[1])) then begin
		Result := parts[0];
		exit;
	end;
	Result := nil;
end;
begin
	secret := 'keepitsecret';
end.