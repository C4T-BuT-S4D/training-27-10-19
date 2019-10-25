﻿// <auto-generated />
using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using chocowrappers.Models;

namespace chocowrappers.Migrations
{
    [DbContext(typeof(ChocoContext))]
    [Migration("20191025080833_FixedFriends")]
    partial class FixedFriends
    {
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .HasAnnotation("ProductVersion", "2.2.6-servicing-10079");

            modelBuilder.Entity("chocowrappers.Models.Chocolate", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd();

                    b.Property<string>("Description");

                    b.Property<string>("Name");

                    b.Property<int?>("UserId");

                    b.HasKey("Id");

                    b.HasIndex("UserId");

                    b.ToTable("Chocolates");
                });

            modelBuilder.Entity("chocowrappers.Models.FriendRelation", b =>
                {
                    b.Property<int>("FromId");

                    b.Property<int>("ToId");

                    b.HasKey("FromId", "ToId");

                    b.HasIndex("ToId");

                    b.ToTable("FriendRelations");
                });

            modelBuilder.Entity("chocowrappers.Models.User", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd();

                    b.Property<string>("Name");

                    b.Property<string>("Password");

                    b.HasKey("Id");

                    b.ToTable("Users");
                });

            modelBuilder.Entity("chocowrappers.Models.Wrapper", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd();

                    b.Property<string>("Name");

                    b.Property<int?>("UserId");

                    b.HasKey("Id");

                    b.HasIndex("UserId");

                    b.ToTable("Wrappers");
                });

            modelBuilder.Entity("chocowrappers.Models.Chocolate", b =>
                {
                    b.HasOne("chocowrappers.Models.User", "User")
                        .WithMany("Chocolates")
                        .HasForeignKey("UserId");
                });

            modelBuilder.Entity("chocowrappers.Models.FriendRelation", b =>
                {
                    b.HasOne("chocowrappers.Models.User", "UserFrom")
                        .WithMany("FriendsTo")
                        .HasForeignKey("FromId")
                        .OnDelete(DeleteBehavior.Cascade);

                    b.HasOne("chocowrappers.Models.User", "UserTo")
                        .WithMany("FriendsFrom")
                        .HasForeignKey("ToId")
                        .OnDelete(DeleteBehavior.Cascade);
                });

            modelBuilder.Entity("chocowrappers.Models.Wrapper", b =>
                {
                    b.HasOne("chocowrappers.Models.User", "User")
                        .WithMany("WrapperCollection")
                        .HasForeignKey("UserId");
                });
#pragma warning restore 612, 618
        }
    }
}
