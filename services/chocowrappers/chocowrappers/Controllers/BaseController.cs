using System.Linq;
using chocowrappers.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace chocowrappers.Controllers
{
    public class BaseController : Controller
    {
        protected ChocoContext Db;
        private User _currentUser;
        private bool _cachedCurrentUser;

        public BaseController(ChocoContext db)
        {
            Db = db;
        }

        protected User GetCurrentUser()
        {
            if (_cachedCurrentUser)
            {
                return _currentUser;
            }

            _cachedCurrentUser = true;
            var username = HttpContext.Items["username"];
            
            if (username == null)
            {
                return _currentUser = null;
            }
            return _currentUser = Db.Users
                .Include(u => u.Chocolates)
                .Include(u => u.WrapperCollection)
                .Include(u => u.FriendsTo).ThenInclude(relation => relation.UserTo)
                .FirstOrDefault(x => x.Name == username.ToString());
        }
        
        public BaseController()
        {
        }
    }
}