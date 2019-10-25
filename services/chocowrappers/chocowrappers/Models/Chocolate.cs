using System.ComponentModel.DataAnnotations.Schema;

namespace chocowrappers.Models
{
    public class Chocolate
    {
        public int Id { get; set; }
        public string Name { get; set;  }
        public string Description { get; set; }

        public int UserId { get; set; }

        [ForeignKey("UserId")]
        public virtual User User { get; set; }
    }
}