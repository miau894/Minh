from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import random
import os

# ID Admin
ADMIN_ID = 6357581712

# Bot Token
TOKEN = "8185028838:AAGV5r4dtEFXCoVrvI0JzaloGOjWyMdGRao"
# Khởi tạo ứng dụng
app = Application.builder().token(TOKEN).build()

# Biến lưu trạng thái user
user_add_mode = {}

# Danh sách người bị ban
banned_users = set()

# Check Admin
def check_admin(update: Update):
    return update.effective_user.id != ADMIN_ID

# Kiểm tra user bị ban
def is_banned(user_id):
    return user_id in banned_users

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_banned(update.effective_user.id):
        return
    user = update.effective_user
    await update.message.reply_text(
        f"\U0001F44B Onii-chan chào bạn {user.first_name} nha~\n"
        "Chào mừng bạn đến với *Bot Hỗ Trợ Tài Khoản & Script*.\n\n"
        "Mình đã sẵn sàng giúp bạn với những lệnh tuyệt vời! \U0001F973\n"
        "Bạn có thể dùng lệnh /help để xem các chức năng có sẵn nhé! ✨\n\n"
        "Hãy thoải mái yêu cầu mình giúp đỡ bất cứ lúc nào, mình luôn ở đây để hỗ trợ bạn \U0001F604\n"
        "Cùng nhau khám phá thế giới bot nào! \U0001F496"
    )

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_banned(update.effective_user.id):
        return
    help_text = (
        "\U0001F4DC Danh sách lệnh hỗ trợ:\n\n"
        "\U0001F3AE /script_bloxfruit - Lấy script Blox Fruit\n"
        "\U0001F3AE /script_deadrail - Lấy script Dead Rail\n"
        "\U0001F6E0️ /add_redfinger - Thêm tài khoản Redfinger (Admin)\n"
        "\U0001F6E0️ /add_ugphone - Thêm tài khoản UGPhone (Admin)\n"
        "\U0001F6E0️ /add_vmos - Thêm tài khoản VMOS (Admin)\n"
        "✅ /get_redfinger - Lấy tài khoản Redfinger (Admin)\n"
        "✅ /get_ugphone - Lấy tài khoản UGPhone (Admin)\n"
        "✅ /get_vmos - Lấy tài khoản VMOS (Admin)\n"
        "\U0001F6D2 /store - Xem số lượng tài khoản lưu (Admin)\n"
        "❓ /help - Xem hướng dẫn"
    )
    await update.message.reply_text(help_text)

# /ban
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if check_admin(update):
        await update.message.reply_text("❌ Bạn không có quyền dùng lệnh này.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("❗ Dùng đúng cú pháp: /ban <user_id>")
        return

    try:
        user_id = int(context.args[0])
        banned_users.add(user_id)
        await update.message.reply_text(f"Onichan đã ban user ID {user_id} vì lý do: xàm lol.")
    except ValueError:
        await update.message.reply_text("❗ ID không hợp lệ.")

# /add_* gộp chung
async def add_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_banned(update.effective_user.id):
        return
    if check_admin(update):
        await update.message.reply_text("❌ Bạn không có quyền dùng lệnh này.")
        return

    command = update.message.text.split("_")[1]
    service = command.lower()

    user_add_mode[update.effective_user.id] = service
    await update.message.reply_text(f"Gửi tài khoản {service.upper()} cần thêm:")

# /get_* gộp chung
async def get_account(update: Update, context: ContextTypes.DEFAULT_TYPE, service: str):
    if is_banned(update.effective_user.id):
        return
    if check_admin(update):
        await update.message.reply_text("❌ Bạn không có quyền dùng lệnh này.")
        return

    filename = f"{service}.txt"

    if not os.path.exists(filename):
        await update.message.reply_text("❗ Chưa có tài khoản lưu.")
        return

    with open(filename, 'r') as f:
        accounts = f.read().splitlines()

    if not accounts:
        await update.message.reply_text("❗ Kho tài khoản trống.")
        return

    account = random.choice(accounts)
    accounts.remove(account)

    with open(filename, 'w') as f:
        f.write("\n".join(accounts))

    await update.message.reply_text(f"\U0001F3AF Tài khoản của bạn:\n{account}")

# Xử lý tin nhắn user gửi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_banned(user_id):
        return
    if user_id not in user_add_mode:
        return

    service = user_add_mode[user_id]
    filename = f"{service}.txt"
    message_text = update.message.text.replace("\n", "").strip()

    if not message_text or "|" not in message_text:
        await update.message.reply_text("❗ Sai cú pháp hoặc tài khoản trống. Vui lòng thử lại.")
        return

    if check_duplicate(filename, message_text):
        await update.message.reply_text("❗ Tài khoản này đã tồn tại. Không thể thêm vào.")
        return

    with open(filename, 'a') as f:
        f.write(message_text + "\n")

    await update.message.reply_text(f"✅ Đã thêm tài khoản vào {service.upper()} thành công!")
    del user_add_mode[user_id]

# Kiểm tra tài khoản trùng
def check_duplicate(filename, account):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            accounts = f.read().splitlines()
            if account in accounts:
                return True
    return False

# /store
async def store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_banned(update.effective_user.id):
        return
    if check_admin(update):
        await update.message.reply_text("❌ Bạn không có quyền dùng lệnh này.")
        return

    redfinger = count_accounts("redfinger.txt")
    ugphone = count_accounts("ugphone.txt")
    vmos = count_accounts("vmos.txt")

    text = (
        "\U0001F6D2 Kho tài khoản hiện tại:\n\n"
        f"🔴 Redfinger: {redfinger} acc\n"
        f"🔵 UGPhone: {ugphone} acc\n"
        f"🟣 VMOS: {vmos} acc"
    )
    await update.message.reply_text(text)

def count_accounts(filename):
    if not os.path.exists(filename):
        return 0
    with open(filename, 'r') as f:
        return len(f.read().splitlines())

# /script_bloxfruit
async def script_bloxfruit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_banned(update.effective_user.id):
        return
    keyboard = [
        [InlineKeyboardButton("\U0001F3AE Redz Hub", callback_data="redz_hub")],
        [InlineKeyboardButton("\U0001F3AE Hoho Hub", callback_data="hoho_hub")],
        [InlineKeyboardButton("\U0001F3AE W Azure", callback_data="w_azure")],
        [InlineKeyboardButton("\U0001F3AE Maru Hub Fake", callback_data="maru_hub")],
        [InlineKeyboardButton("\U0001F3AE Xero Hub", callback_data="xero_hub")],
        [InlineKeyboardButton("\U0001F3AE Min Gaming", callback_data="min_gaming")]
    ]
    await update.message.reply_text("\U0001F3AE Chọn script Blox Fruit:", reply_markup=InlineKeyboardMarkup(keyboard))

# /script_deadrail
async def script_deadrail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_banned(update.effective_user.id):
        return
    keyboard = [
        [InlineKeyboardButton("\U0001F682 DeadRail Hub", callback_data="deadrail_hub")],
        [InlineKeyboardButton("\U0001F682 Tbao Hub", callback_data="tbao_hub")],
        [InlineKeyboardButton("\U0001F682 Neox Hub", callback_data="neox_hub")],
        [InlineKeyboardButton("\U0001F682 Auto Win", callback_data="auto_win")],
        [InlineKeyboardButton("\U0001F682 Speed X Hub", callback_data="speed_x_hub")]
    ]
    await update.message.reply_text("\U0001F682 Chọn script Dead Rail:", reply_markup=InlineKeyboardMarkup(keyboard))

# Xử lý callback
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    scripts = {
        "redz_hub": '''-- Official Redz
loadstring(game:HttpGet("https://raw.githubusercontent.com/newredz/BloxFruits/refs/heads/main/Source.luau"))()''',
        "hoho_hub": '''-- Hoho Hub
loadstring(game:HttpGet("https://raw.githubusercontent.com/acsu123/HOHO_H/main/Loading_UI"))()''',
        "w_azure": '''-- W Azure
loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/3b2169cf53bc6104dabe8e19562e5cc2.lua"))()''',
        "maru_hub": '''-- Maru Hub Fake
getgenv().Team = "Marines"
loadstring(game:HttpGet("https://raw.githubusercontent.com/LuaCrack/KimP/refs/heads/main/MaruHub"))()''',
        "xero_hub": '''-- Xero Hub
getgenv().Team = "Marines"
getgenv().Hide_Menu = false
getgenv().Auto_Execute = false
loadstring(game:HttpGet("https://raw.githubusercontent.com/Xero2409/XeroHub/refs/heads/main/main.lua"))()''',
        "min_gaming": '''-- Min Gaming
loadstring(game:HttpGet("https://raw.githubusercontent.com/LuaCrack/Min/refs/heads/main/MinA1Eng"))()''',
        "deadrail_hub": '''-- DeadRail Hub
loadstring(game:HttpGet("https://pastebin.com/raw/DeadrHub"))()''',
        "tbao_hub": '''-- Tbao Hub
loadstring(game:HttpGet("https://pastebin.com/raw/TbaoHub"))()''',
        "neox_hub": '''-- Neox Hub
loadstring(game:HttpGet("https://raw.githubusercontent.com/hassanxzayn-lua/NEOXHUBMAIN/refs/heads/main/loader", true))()''',
        "auto_win": '''-- Auto Win
loadstring(game:HttpGet("https://raw.githubusercontent.com/gumanba/Scripts/refs/heads/main/DeadRails", true))()''',
        "speed_x_hub": '''-- Speed X Hub
loadstring(game:HttpGet("https://raw.githubusercontent.com/AhmadV99/Speed-Hub-X/main/Speed%20Hub%20X.lua", true))()'''
    }

    if query.data in scripts:
        await query.edit_message_text(f"Đây là script {query.data.replace('_', ' ').title()}:\n\n{scripts[query.data]}")

# Main
def main():
    print("Bot đã khởi động!")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add_redfinger", add_account))
    app.add_handler(CommandHandler("add_ugphone", add_account))
    app.add_handler(CommandHandler("add_vmos", add_account))
    app.add_handler(CommandHandler("get_redfinger", lambda u, c: get_account(u, c, "redfinger")))
    app.add_handler(CommandHandler("get_ugphone", lambda u, c: get_account(u, c, "ugphone")))
    app.add_handler(CommandHandler("get_vmos", lambda u, c: get_account(u, c, "vmos")))
    app.add_handler(CommandHandler("store", store))
    app.add_handler(CommandHandler("script_bloxfruit", script_bloxfruit))
    app.add_handler(CommandHandler("script_deadrail", script_deadrail))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()
