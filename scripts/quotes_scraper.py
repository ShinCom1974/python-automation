import asyncio
import logging
import random
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("scraper.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

TARGET_URL = "https://quotes.toscrape.com/js"
BASE_URL = "https://quotes.toscrape.com"
USER_AGENT = "Mozilla/5.0 (compatible; PythonScraper/1.0)"


def is_scraping_allowed(base_url: str, target_url: str) -> bool:
    """robots.txt を確認してスクレイピングが許可されているか返す。取得失敗時は許可とみなす。"""
    robots_url = urljoin(base_url, "/robots.txt")
    try:
        resp = requests.get(robots_url, timeout=10, headers={"User-Agent": USER_AGENT})
        resp.raise_for_status()
        rp = RobotFileParser()
        rp.parse(resp.text.splitlines())
        allowed = rp.can_fetch(USER_AGENT, target_url)
        logger.info(f"robots.txt を読み込みました: {robots_url}")
        return allowed
    except requests.RequestException as e:
        logger.warning(f"robots.txt の読み込みに失敗しました ({e})。アクセス許可として扱います。")
        return True


def random_sleep(min_sec: float = 1.0, max_sec: float = 3.0) -> None:
    wait = random.uniform(min_sec, max_sec)
    logger.info(f"待機中: {wait:.2f}秒")
    time.sleep(wait)


async def scrape() -> None:
    date_str = datetime.now().strftime("%Y%m%d")
    output_dir = Path(__file__).parent.parent
    md_path = output_dir / f"quotes_{date_str}.md"
    png_path = output_dir / f"quotes_{date_str}.png"

    # robots.txt チェック
    if not is_scraping_allowed(BASE_URL, TARGET_URL):
        logger.error(f"robots.txt によりアクセスが禁止されています: {TARGET_URL}")
        return

    logger.info(f"アクセス許可確認済み: {TARGET_URL}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(user_agent=USER_AGENT)

        try:
            logger.info(f"ページにアクセス中: {TARGET_URL}")
            await page.goto(TARGET_URL, timeout=30000)

            # JavaScriptによる描画完了を待機
            await page.wait_for_selector(".quote", timeout=15000)
            logger.info("ページの読み込み・JS描画完了")

            # リクエスト間の待機
            random_sleep()

            # 名言を取得
            quote_elements = await page.query_selector_all(".quote")
            results = []
            for el in quote_elements:
                text_el = await el.query_selector(".text")
                author_el = await el.query_selector(".author")
                if text_el and author_el:
                    text = await text_el.inner_text()
                    author = await author_el.inner_text()
                    results.append({"text": text.strip(), "author": author.strip()})

            logger.info(f"{len(results)}件の名言を取得しました")

            # スクリーンショット保存
            await page.screenshot(path=str(png_path), full_page=True)
            logger.info(f"スクリーンショット保存: {png_path.name}")

            # Markdown 生成・保存
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            lines = [
                f"# Quotes — {date_str}",
                "",
                f"収集日時: {now_str}  ",
                f"収集元: {TARGET_URL}",
                "",
                "---",
                "",
            ]
            for i, q in enumerate(results, 1):
                lines.append(f"## {i}. {q['author']}")
                lines.append("")
                lines.append(f"> {q['text']}")
                lines.append("")

            md_path.write_text("\n".join(lines), encoding="utf-8")
            logger.info(f"Markdown保存: {md_path.name}")

        except PlaywrightTimeoutError:
            logger.error("接続タイムアウトエラーが発生しました。ネットワーク接続またはサイトの状態を確認してください。")
        except requests.ConnectionError:
            logger.error("接続エラーが発生しました。ネットワーク接続を確認してください。")
        except Exception as e:
            logger.error(f"予期しないエラーが発生しました: {e}")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(scrape())
