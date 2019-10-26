program main;

uses System;
uses System.Net;
uses System.Text;
uses System.Threading.Tasks;
uses router;
uses handlers;

var router: HttpRouter;

begin
  router := new HttpRouter();
  router.Register('/', HandleRoot);
  router.Register('/registerForm', HandleRegister);
  router.Register('/loginForm', HandleLogin);
  router.Register('/icecreams', HandleIcecreams);
  router.Register('/addForm', HandleAddIcecream);
  router.Register('/lastusers', HandleLastUsers);

  var server := new HttpListener();
  server.Prefixes.Add('http://*:5555/');
  server.Start();
  WriteLn('Waiting for connections');
  while True do
  begin
    var requestTask := server.GetContextAsync();
    var req := requestTask.Result;
    try
      router.Serve(req);
    except on System.Exception do begin
      req.Response.StatusCode := 500;
      req.Response.Close();
      end;
    end;
  end;

end.
