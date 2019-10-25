using System;
using System.Security.Cryptography;
using System.Text;
using chocowrappers.AppData;

namespace chocowrappers.Helpers
{
    public static class AuthHelper
    {
        public static string CalcSignature(string data)
        {
            var toHash = AuthData.SecretKey + data;
            var md5 = MD5.Create();
            var hash = md5.ComputeHash(Encoding.UTF8.GetBytes(toHash));
            return Convert.ToBase64String(hash);
        }

        public static bool IsSessionValid(string session, string signature)
        {
            return CalcSignature(session) == signature;
        }
    }
}