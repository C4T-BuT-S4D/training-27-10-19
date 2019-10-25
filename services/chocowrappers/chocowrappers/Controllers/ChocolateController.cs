using System.Data;
using System.Linq;
using chocowrappers.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace chocowrappers.Controllers
{
    public class ChocolateController: BaseController
    {
        public ChocolateController(ChocoContext db) : base(db)
        {
        }
        public IActionResult ViewChocolate(int id)
        {
            if (GetCurrentUser() == null)
            {
                return RedirectToAction("Login", "User");
            }
            var choco = Db.Chocolates
                .Include(c => c.User).ThenInclude(u => u.FriendsFrom)
                .FirstOrDefault(x => x.Id == id);
            if (choco == null)
            {
                return NotFound();
            }

            if (choco.UserId == GetCurrentUser().Id)
            {
                return View(choco);
            }

            var rel = choco.User.FriendsFrom.FirstOrDefault(r => r.FromId == GetCurrentUser().Id);
            if (rel != null)
            {
                return View(choco);
            }
            
            return NotFound();   
        }

        [HttpGet]
        public IActionResult Create()
        {
            if (GetCurrentUser() == null)
            {
                return RedirectToAction("Login", "User");
            }
            return View();
        }
        
        [HttpPost]
        public IActionResult CreatePost(Chocolate choco)
        {
            if (GetCurrentUser() == null)
            {
                return RedirectToAction("Login", "User");
            }
            
            try
            {
                if (ModelState.IsValid)
                {
                    if (choco.UserId == 0)
                    {
                        choco.UserId = GetCurrentUser().Id;
                    }
                    Db.Chocolates.Add(choco);
                    Db.SaveChanges();
                    return RedirectToAction("Index", "Home");
                }
            }
            catch (DataException)
            {
                ModelState.AddModelError("", "Unable to save changes. Try again, and if the problem persists see your system administrator.");
            }

            return View("Create", choco);
        }
    }
}