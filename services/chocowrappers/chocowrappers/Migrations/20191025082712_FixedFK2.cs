using Microsoft.EntityFrameworkCore.Migrations;

namespace chocowrappers.Migrations
{
    public partial class FixedFK2 : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Chocolates_Users_UserId",
                table: "Chocolates");

            migrationBuilder.AlterColumn<int>(
                name: "UserId",
                table: "Chocolates",
                nullable: false,
                oldClrType: typeof(int),
                oldNullable: true);

            migrationBuilder.AddForeignKey(
                name: "FK_Chocolates_Users_UserId",
                table: "Chocolates",
                column: "UserId",
                principalTable: "Users",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Chocolates_Users_UserId",
                table: "Chocolates");

            migrationBuilder.AlterColumn<int>(
                name: "UserId",
                table: "Chocolates",
                nullable: true,
                oldClrType: typeof(int));

            migrationBuilder.AddForeignKey(
                name: "FK_Chocolates_Users_UserId",
                table: "Chocolates",
                column: "UserId",
                principalTable: "Users",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);
        }
    }
}
