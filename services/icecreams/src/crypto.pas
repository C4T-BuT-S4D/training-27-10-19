Unit crypto;

function Createmd5(input: string): string;
var 
	i: integer;
	res: string;
begin
	var md5 := System.Security.Cryptography.MD5.Create();
	var bytes := Encoding.ASCII.GetBytes(input);
	var hashed := md5.ComputeHash(bytes);
	for i := 0 to Length(hashed) - 1 do 
		res += hashed[i].ToString('x2');
	Result := res;
end;

end.