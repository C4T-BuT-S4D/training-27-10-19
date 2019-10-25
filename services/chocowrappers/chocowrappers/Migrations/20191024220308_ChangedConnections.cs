using Microsoft.EntityFrameworkCore.Migrations;

namespace chocowrappers.Migrations
{
    public partial class ChangedConnections : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Chocolates_Users_UserId",
                table: "Chocolates");

            migrationBuilder.DropForeignKey(
                name: "FK_Wrappers_Users_UserId",
                table: "Wrappers");

            migrationBuilder.AlterColumn<int>(
                name: "UserId",
                table: "Wrappers",
                nullable: true,
                oldClrType: typeof(int));

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

            migrationBuilder.AddForeignKey(
                name: "FK_Wrappers_Users_UserId",
                table: "Wrappers",
                column: "UserId",
                principalTable: "Users",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Chocolates_Users_UserId",
                table: "Chocolates");

            migrationBuilder.DropForeignKey(
                name: "FK_Wrappers_Users_UserId",
                table: "Wrappers");

            migrationBuilder.AlterColumn<int>(
                name: "UserId",
                table: "Wrappers",
                nullable: false,
                oldClrType: typeof(int),
                oldNullable: true);

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

            migrationBuilder.AddForeignKey(
                name: "FK_Wrappers_Users_UserId",
                table: "Wrappers",
                column: "UserId",
                principalTable: "Users",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }
    }
}
