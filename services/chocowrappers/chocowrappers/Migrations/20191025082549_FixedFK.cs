using Microsoft.EntityFrameworkCore.Migrations;

namespace chocowrappers.Migrations
{
    public partial class FixedFK : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Wrappers_Users_UserId",
                table: "Wrappers");

            migrationBuilder.AlterColumn<int>(
                name: "UserId",
                table: "Wrappers",
                nullable: false,
                oldClrType: typeof(int),
                oldNullable: true);

            migrationBuilder.AddForeignKey(
                name: "FK_Wrappers_Users_UserId",
                table: "Wrappers",
                column: "UserId",
                principalTable: "Users",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Wrappers_Users_UserId",
                table: "Wrappers");

            migrationBuilder.AlterColumn<int>(
                name: "UserId",
                table: "Wrappers",
                nullable: true,
                oldClrType: typeof(int));

            migrationBuilder.AddForeignKey(
                name: "FK_Wrappers_Users_UserId",
                table: "Wrappers",
                column: "UserId",
                principalTable: "Users",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);
        }
    }
}
