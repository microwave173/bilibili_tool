from playwright.sync_api import sync_playwright
import json

def get_and_save_cookies(save_path="bilibili_cookies.json"):
    # 启动 Playwright
    with sync_playwright() as p:
        print("正在启动 Playwright 浏览器...")
        
        # 启动 Chromium，headless=False 代表显示浏览器图形界面
        browser = p.chromium.launch(headless=False)
        
        # 创建一个独立的浏览器上下文（类似打开一个无痕模式的新窗口，非常干净）
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # 访问 B 站
            page.goto("https://www.bilibili.com")
            
            # 提示用户手动操作
            print("\n" + "="*50)
            print("浏览器已打开。请在弹出的窗口中手动登录 Bilibili。")
            print("【注意】请在完全登录成功（能看到自己的头像和历史记录）后，再进行下一步操作！")
            print("="*50 + "\n")
            
            # 阻塞程序，等待你手动扫码/密码登录完成
            input(">>> 登录完成后，请在此处按下 Enter 键以保存 Cookie...")
            
            # 从当前的浏览器上下文中提取所有 Cookie
            cookies = context.cookies()
            
            # 将 Cookie 写入 JSON 文件
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(cookies, f, ensure_ascii=False, indent=4)
                
            print(f"\n✅ 成功！Cookie 已提取并保存至: {save_path}")

        except Exception as e:
            print(f"\n❌ 运行过程中出现错误: {e}")

        finally:
            print("正在关闭浏览器...")
            # 自动关闭浏览器，释放资源
            browser.close()

if __name__ == "__main__":
    get_and_save_cookies()