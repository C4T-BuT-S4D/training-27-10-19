using System.Data;
using System.Linq;
using chocowrappers.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace chocowrappers.Controllers
{
    public class WrapperController: BaseController
    {
        public WrapperController(ChocoContext db) : base(db)
        {
        }
        public IActionResult ViewWrapper(int id)
        {
            var wrapper = Db.Wrappers.Include(w => w.User).FirstOrDefault(x => x.Id == id);
            if (wrapper == null || wrapper.User != GetCurrentUser())
            {
                return NotFound();
            }
            return View(wrapper);
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
        public IActionResult CreatePost(Wrapper wrapper)
        {
            if (GetCurrentUser() == null)
            {
                return RedirectToAction("Login", "User");
            }
            
            try
            {
                if (ModelState.IsValid)
                {
                    if (wrapper.UserId == 0)
                    {
                        wrapper.UserId = GetCurrentUser().Id;
                    }
                    Db.Wrappers.Add(wrapper);
                    Db.SaveChanges();
                    return RedirectToAction("Index", "Home");
                }
            }
            catch (DataException)
            {
                ModelState.AddModelError("", "Unable to save changes. Try again, and if the problem persists see your system administrator.");
            }

            return View("Create", wrapper);
        }
    }
}