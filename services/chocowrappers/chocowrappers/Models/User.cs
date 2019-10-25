using System.Collections;
using System.Collections.Generic;

namespace chocowrappers.Models
{
    public class User
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Password { get; set; }
        public virtual ICollection<Chocolate> Chocolates { get; set; }
        public virtual ICollection<Wrapper> WrapperCollection { get; set; }

        public virtual ICollection<FriendRelation> FriendsFrom { get; set; }
        public virtual ICollection<FriendRelation> FriendsTo { get; set; }
    }

    public class FriendRelation
    {
        public int FromId { get; set; }
        public int ToId { get; set; }

        public virtual User UserFrom { get; set; }
        public virtual User UserTo { get; set; }
    }
}