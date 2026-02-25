import requests
import json
import re

def download_bilibili_media():
    # 1. 获取用户输入（已修改提示语）
    target_url = input("请输入 B 站视频网址 (例如 https://www.bilibili.com/video/BV...): ").strip()
    save_name = input("请输入保存的文件名 (【无需输入后缀名】，例如 spongebob_clip): ").strip()

    # 2. 初始化 Session 并设置必须的 Headers
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": target_url 
    }
    session.headers.update(headers)

    # 3. 加载 Playwright 保存的 Cookie
    try:
        with open("bilibili_cookies.json", "r", encoding="utf-8") as f:
            cookie_list = json.load(f)
            for cookie in cookie_list:
                session.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain', ''))
        print("✅ Cookie 加载成功！")
    except FileNotFoundError:
        print("❌ 找不到 bilibili_cookies.json 文件，请先运行 Playwright 脚本生成。")
        return

    # 4. 访问页面获取 HTML
    print("\n正在获取视频页面数据...")
    response = session.get(target_url)
    html_content = response.text

    # 5. 正则匹配 Video 和 Audio 的 base_url
    # 匹配画面流
    video_match = re.search(r'"video":.*?\[.*?\{.*?"base_url":"([^"]+)"', html_content)
    # 匹配音频流
    audio_match = re.search(r'"audio":.*?\[.*?\{.*?"base_url":"([^"]+)"', html_content)
    
    if not video_match or not audio_match:
        print("❌ 未能在页面中完整匹配到视频或音频直链。")
        print("可能是由于页面没有完全加载，或者目标视频需要大会员而 Cookie 权限不足。")
        return

    # 提取并处理 B 站 JSON 中的转义字符 (\u0026 -> &)
    video_base_url = video_match.group(1).encode('utf-8').decode('unicode_escape')
    audio_base_url = audio_match.group(1).encode('utf-8').decode('unicode_escape')
    print("✅ 成功提取到视频与音频直链！")

    # 6. 定义一个通用的下载函数
    def download_file(url, file_path, media_type):
        print(f"正在下载 {media_type}，保存为 {file_path} ...")
        res = session.get(url, stream=True)
        if res.status_code == 200:
            with open(file_path, "wb") as f:
                for chunk in res.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
            print(f"🎉 {media_type} 下载完成: {file_path}")
        else:
            print(f"❌ {media_type} 下载失败，状态码: {res.status_code}")

    # 7. 开始分别下载
    print("\n" + "="*40)
    download_file(video_base_url, f"{save_name}.mp4", "画面 (Video)")
    download_file(audio_base_url, f"{save_name}.mp3", "音频 (Audio)")
    print("="*40 + "\n全部任务执行完毕！")

if __name__ == "__main__":
    download_bilibili_media()