Unit handlers;

uses System.IO;
uses System.Net;
uses controllers;
uses session;

procedure writeHtml(var ctx: System.Net.HttpListenerContext; content: string);
begin
	ctx.Response.ContentType := 'text/html';
	ctx.Response.ContentLength64 := Length(content);
	var sw := new StreamWriter(ctx.Response.OutputStream);
	sw.WriteLine(content);
	sw.Close();
end;

procedure redirect(var ctx: System.Net.HttpListenerContext; path: string);
begin
	ctx.Response.Redirect(path);
	ctx.Response.Close();
end;


procedure notFound(var ctx: System.Net.HttpListenerContext);
begin
	ctx.Response.StatusCode := 404;
	writeHtml(ctx, '<h3>404 not found</h3>')
end;

function getContentType(ext: string): string;
begin
	case ext of
		'jpg': Result := 'image/jpeg';
		'html': Result := 'text/html';
		'css': Result := 'text/css';
		'ico': Result := 'image/x-icon';
	else
		Result := 'text/plain';
	end;
end;


procedure serveStatic(var ctx: System.Net.HttpListenerContext; ext: string);
begin
	var filePath := '.' + ctx.Request.Url.LocalPath;
	if not FileExists(filePath) then begin notFound(ctx); exit; end;

	ctx.Response.ContentType := getContentType(ext);
	var fileInfo := new System.IO.FileInfo(filepath);
	ctx.Response.ContentLength64 := fileInfo.Length;
	var sr := new FileStream(filepath, FileMode.Open);
    var buffer := new byte[4096];
    var len := sr.Read(buffer, 0, Length(buffer));
    while (len > 0) do begin
    	ctx.Response.OutputStream.Write(buffer,0, len);
    	len := sr.Read(buffer, 0, Length(buffer));
    end;
    sr.Close();
	ctx.Response.OutputStream.Close();
end;

procedure HandleIcecreams(var ctx: System.Net.HttpListenerContext);
begin
	var user := GetUserSession(ctx);
	if (user = nil) then begin redirect(ctx, '/login.html'); exit; end;
	writeHtml(ctx, 'Your icecreams: <br>' + GetIcecreams(user));
end;

procedure HandleAddIcecream(var ctx: System.Net.HttpListenerContext);
begin
	var user := GetUserSession(ctx);
	if (user = nil) then begin redirect(ctx, '/login.html'); exit; end;
	var getParams := ctx.Request.QueryString;
	var icecream := getParams['icecream'];
	if ((icecream = nil) or (icecream = '')) then begin writeHtml(ctx, 'Fill the form please'); exit; end;
	AddIcecream(user, icecream);
	writeHtml(ctx, 'Icecream added successfully');
end;

procedure HandleRegister(var ctx: System.Net.HttpListenerContext);
begin
	var getParams := ctx.Request.QueryString;
	var login := getParams['login'];
	var password := getParams['password'];
	if ((login = nil) or (login = '') or (password = nil) or (password = '')) then begin writeHtml(ctx, 'Fill the form please'); exit; end;
	if (GetUser(login) <> nil) then begin writeHtml(ctx, 'User with this username already exists'); exit; end;
	AddUser(login, password);
	LoginSession(login, ctx);
	redirect(ctx, '/index.html');
end;

procedure HandleLogin(var ctx: System.Net.HttpListenerContext);
begin
	var getParams := ctx.Request.QueryString;
	var login := getParams['login'];
	var password := getParams['password'];
	if ((login = nil) or (login = '') or (password = nil) or (password = '')) then begin writeHtml(ctx, 'Fill the form please'); exit; end;
	if (GetUser(login) <> password) then begin writeHtml(ctx, 'Incorrect login or password'); exit; end;
	LoginSession(login, ctx);
	redirect(ctx, '/index.html');
end;

procedure HandleLastUsers(var ctx: System.Net.HttpListenerContext);
begin
	writeHtml(ctx, 'Last 40 users: <br>' + GetLastUsers(40));
end;


procedure HandleRoot(var ctx: System.Net.HttpListenerContext);
begin
	if (ctx.Request.Url.LocalPath = '/') then begin
		redirect(ctx, '/index.html');
		exit; 
	end;
	var parts := ctx.Request.Url.ToString().Split('.');
	var ext := parts[Length(parts) - 1];
	case ext of
	'jpg','html','css','ico': serveStatic(ctx, ext);
	else
		notFound(ctx);
	end;
end;


end.