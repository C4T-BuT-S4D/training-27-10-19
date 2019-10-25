using System;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using chocowrappers.Helpers;
using chocowrappers.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace chocowrappers.Controllers
{
    public class UserController : BaseController
    {
        public UserController(ChocoContext db) : base(db)
        {
        }

        [HttpGet]
        public IActionResult Register()
        {
            return View();
        }

        [HttpPost]
        public IActionResult RegisterPost()
        {
            var username = Request.Form["username"].ToString();
            var password = Request.Form["password"].ToString();

            if (username == "" || password == "")
            {
                return BadRequest("need to provide username and password");
            }

            var user = Db.Users.FirstOrDefault(x => x.Name == username);
            if (user != null)
            {
                return BadRequest("user with this username already registered");
            }

            Db.Users.Add(new User {Name = username, Password = password});
            Db.SaveChanges();

            return RedirectToAction("Login");
        }

        [HttpGet]
        public IActionResult Login()
        {
            return View();
        }

        [HttpPost]
        public IActionResult LoginPost()
        {
            var username = Request.Form["username"].ToString();
            var password = Request.Form["password"].ToString();

            var user = Db.Users.FirstOrDefault(x => x.Name == username && x.Password == password);
            if (user == null)
            {
                return BadRequest("invalid credentials");
            }

            var authCookieString = user.Id + "." + user.Name;
            var signatureCookieString = AuthHelper.CalcSignature(authCookieString);

            var option = new CookieOptions();
            option.Expires = DateTime.Now.AddHours(24);
            HttpContext.Response.Cookies.Append("session", authCookieString, option);
            HttpContext.Response.Cookies.Append("sign", signatureCookieString, option);

            return RedirectToAction("Index", "Home");
        }

        public IActionResult Logout()
        {
            foreach (var cookie in Request.Cookies.Keys)
            {
                Response.Cookies.Delete(cookie);
            }

            return RedirectToAction("Index", "Home");
        }

        public IActionResult Me()
        {
            if (GetCurrentUser() == null)
            {
                return RedirectToAction("Login");
            }

            return View(GetCurrentUser());
        }

        public IActionResult ViewUser(int id)
        {
            if (GetCurrentUser() != null && id == GetCurrentUser().Id)
            {
                return RedirectToAction("Me");
            }

            var user = Db.Users
                .Include(x => x.Chocolates)
                .FirstOrDefault(x => x.Id == id);
            if (user == null)
            {
                return NotFound();
            }

            return View(user);
        }

        public IActionResult List()
        {
            var users = Db.Users.ToList();
            return View(users);
        }

        [HttpGet]
        public IActionResult AddToFriendsRequest(int id)
        {
            if (GetCurrentUser() == null)
            {
                return RedirectToAction("Login");
            }

            var friend = Db.Users.FirstOrDefault(x => x.Id == id);
            if (friend == null)
            {
                return NotFound();
            }

            return View(friend);
        }

        [HttpPost]
        public IActionResult AddToFriends(int id, string guesses)
        {
            if (GetCurrentUser() == null)
            {
                return RedirectToAction("Login");
            }

            var wrapperNames = guesses.Split(",");
            if (wrapperNames.Length > 100)
            {
                return BadRequest("100 guesses maximum");
            }

            var friend = Db.Users.Include(u => u.WrapperCollection).FirstOrDefault(x => x.Id == id);
            if (friend == null)
            {
                return NotFound();
            }

            var rel = Db.FriendRelations.FirstOrDefault(r =>
                r.FromId == GetCurrentUser().Id && r.ToId == friend.Id);
            if (rel != null)
            {
                return BadRequest("Already friends!");
            }

            var cnt = 0;
            foreach (var item in friend.WrapperCollection)
            {
                if (wrapperNames.Contains(item.Name))
                {
                    cnt += 1;
                }
            }

            if (cnt * 2 <= friend.WrapperCollection.Count)
            {
                return BadRequest("You don't know this user, go away!");
            }

            var relation = new FriendRelation {FromId = GetCurrentUser().Id, ToId = id};
            Db.FriendRelations.Add(relation);
            Db.SaveChanges();

            return RedirectToAction("ViewUser", new {id});
        }
    }
}