using System;
using Microsoft.EntityFrameworkCore;

namespace chocowrappers.Models
{
    public sealed class ChocoContext : DbContext
    {
        public DbSet<User> Users { get; set; }
        public DbSet<FriendRelation> FriendRelations { get; set; }
        public DbSet<Chocolate> Chocolates { get; set; }
        public DbSet<Wrapper> Wrappers { get; set; }

        public ChocoContext(DbContextOptions options) : base(options)
        {
            Database.EnsureCreated();
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<User>().HasMany(u => u.Chocolates).WithOne(c => c.User);
            modelBuilder.Entity<User>().HasMany(u => u.WrapperCollection).WithOne(w => w.User);

            modelBuilder.Entity<FriendRelation>().HasKey(rel => new {rel.FromId, rel.ToId});

            modelBuilder.Entity<FriendRelation>()
                .HasOne(e => e.UserFrom)
                .WithMany(e => e.FriendsTo)
                .HasForeignKey(e => e.FromId);

            modelBuilder.Entity<FriendRelation>()
                .HasOne(e => e.UserTo)
                .WithMany(e => e.FriendsFrom)
                .HasForeignKey(e => e.ToId);
        }
    }
}