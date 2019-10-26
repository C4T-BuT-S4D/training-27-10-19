Unit router;

uses System;
uses System.Net;
uses System.Threading.Tasks;

type 
	HandlerFunc = procedure(var ctx: System.Net.HttpListenerContext);
	HttpRouter = class
private
	handlers: Dictionary<string, HandlerFunc>;
	prefixes: List<string>;
public
	constructor Create();
	begin
		prefixes := new List<string>;
		handlers := new Dictionary<string, HandlerFunc>
	end;
	procedure Register(prefix :string; handler: HandlerFunc);
	begin
		prefixes.Add(prefix);
		prefixes.Sort();
		prefixes.Reverse();
		handlers.Add(prefix, handler);
	end;
	procedure Serve(var ctx: System.Net.HttpListenerContext);
	begin
		var url := ctx.Request.Url.LocalPath;
		{ Exact match. }
		if handlers.ContainsKey(url) then begin
			handlers[url](ctx);
			exit;
		end;
		foreach var p in prefixes do begin
			if (url.StartsWith(p)) then begin 
				handlers[p](ctx);
				break;
			end;
		end;
	end;
end;

end.