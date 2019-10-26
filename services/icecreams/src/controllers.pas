Unit controllers;

uses crypto;
var 
	mtx: System.Threading.Mutex;


function GetUser(login: string): string;
begin
	Result := nil;
	foreach var s in ReadLines('data/users.txt') do
	begin
		var ss := s.ToWords;
		if (ss[0] = login) then begin
			Result := ss[1];
		end;
	end;
end;

function GetLastUsers(n: integer): string;
begin
	var st := new Queue<string>;
	foreach var s in ReadLines('data/users.txt') do
	begin
		var ss := s.ToWords;
		st.Enqueue(ss[0]);
		if (st.Count > n) then st.Dequeue;
	end;
	while (st.Count <> 0) do  Result += st.Dequeue + '<br>'
end;

procedure AddUser(login,password: string);
begin
	{I don't know why append is not atomic in .NET (but should for small chunks).}
	mtx.WaitOne();
	var f := OpenAppend('data/users.txt');
	WriteLn(f, login, ' ', password);
	Close(f);
	mtx.ReleaseMutex();
end;

function GetIcecreams(login: string): string;
begin
	var fname := 'data/' + CreateMd5(login) + '.txt';
	if not FileExists(fname) then Result := 'Still no icecreams' else
	foreach var s in ReadLines(fname) do
		Result += s + '</br>'
end;

procedure AddIcecream(login: string; icecream: string);
begin
	var fname := 'data/' + CreateMd5(login) + '.txt';
	var f := OpenAppend(fname);
	WriteLn(f, icecream);
	Close(f);
end;
begin
	mtx := new System.Threading.Mutex();
end.