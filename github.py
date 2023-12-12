#      __  __            
#     |  \/  | ___  _ __ 
#     | |\/| |/ _ \| '__|
#     | |  | | (_) | |   
#     |_|  |_|\___/|_|    

# Code is licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# https://creativecommons.org/licenses/by-nc-nd/4.0/
# You CANNOT edit this file without direct permission from the author.
# You can redistribute this file without any changes.

# meta developer: @morflenmods
# scope: hikka_min 1.6.2

import requests
from hikkatl.tl.types import Message
from .. import loader, utils

@loader.tds
class GitHubMod(loader.Module):
    """Модуль для просмотра профиля GitHub, для просмотра информации репозиториев."""

    strings_ru = {
        "name": "Github",
        "profile_info": "<b>Информация профиля: </b>",
        "repo_info": "<b>Информация репозитория: </b>",
        "invalid_link": (
            "<b><emoji document_id=5978859389614821335>❌</emoji>Неверная ссылка Github."
            "Верные ссылки Github начинаются с: https://github.com...</b>"
        ),
        "user_not_found": (
            "<b><emoji document_id=5978859389614821335>❌</emoji>Пользователь не найден.</b>"
        ),
        "repo_not_found": (
            "<b><emoji document_id=5978859389614821335>❌</emoji>Репозиторий не найден.</b>"
        ),
    }

    @loader.command(ru_doc="<profile / url> - Поиск информации по профилю Github")
    async def gitprof(self, message: Message):
        """<profile / url> - Fetch information about GitHub profile"""
        if not (link := utils.get_args_raw(message)):
            await utils.answer(message, self.strings["invalid_link"])
            return

        if link.startswith("https://github.com/"):
            username = link.split("/")[3]

        try:
            response = await utils.run_sync(
                requests.get, f"https://api.github.com/users/{username}"
            )
            response.raise_for_status()
            user_data = response.json()
            info_text = (
                f"{self.strings['profile_info']}\n\n<b><emoji"
                " document_id=5348544647977254780>🔍</emoji>Ссылка:</b>"
                f" {link}\n<b><emoji"
                " document_id=5222465715499446573>🌐</emoji>Юзернейм:</b>"
                f" {user_data.get('login', 'N/A')}\n<b><emoji"
                " document_id=5222465715499446573>🌐</emoji>Имя:</b>"
                f" {user_data.get('name', 'N/A')}\n<b><emoji"
                " document_id=5222030772751314651>🖌</emoji>Био:</b>"
                f" {user_data.get('bio', 'N/A')}\n<b><emoji"
                " document_id=5350469811233110106>🌎</emoji>Местоположение:</b>"
                f" {user_data.get('location', 'N/A')}\n<b><emoji"
                " document_id=5222473609649337576>🔥</emoji>Подписчики:</b>"
                f" {user_data.get('followers', 'N/A')}\n<b><emoji"
                " document_id=5221962650275034448>❤️</emoji>Подписался:</b>"
                f" {user_data.get('following', 'N/A')}\n<b><emoji"
                " document_id=5345987742276797245>📁</emoji>Публичные репозитории:</b>"
                f" {user_data.get('public_repos', 'N/A')}\n"
            )

            if avatar_url := user_data.get("avatar_url"):
                await utils.answer_file(
                    message,
                    avatar_url,
                    info_text,
                    link_preview=False,
                )
            else:
                await utils.answer(message, info_text)
        except Exception:
            await utils.answer(message, self.strings["user_not_found"])

    @loader.command(ru_doc="Просмотр информации о репозитории Github")
    async def gitrepo(self, message: Message):
        """Fetch information about GitHub repository"""
        if not (link := utils.get_args_raw(message)):
            await utils.answer(message, self.strings["invalid_link"])
            return

        if link.startswith("https://github.com/"):
            parts = link.split("/")
            if len(parts) >= 5:
                username = parts[3]
                repo_name = parts[4]
        elif len(link.split("/")) == 2:
            username, repo_name = link.split("/")

        try:
            response = await utils.run_sync(
                requests.get, f"https://api.github.com/repos/{username}/{repo_name}"
            )
            response.raise_for_status()
            repo_data = response.json()
            info_text = (
                f"{self.strings['repo_info']}\n\n<b><emoji"
                " document_id=5348544647977254780>🔍</emoji>Ссылка:</b>"
                f" {link}\n<b><emoji"
                " document_id=5345987742276797245>📁</emoji>Репозиторий:</b>"
                f" {repo_data.get('name', 'N/A')}\n<b><emoji"
                " document_id=5222030772751314651>🖌</emoji>Описание:</b>"
                f" {repo_data.get('description', 'N/A')}\n<b><emoji"
                " document_id=5350469811233110106>🌎</emoji>Язык:</b>"
                f" {repo_data.get('language', 'N/A')}\n<b><emoji"
                " document_id=5350324387935434521>🌠</emoji>Звёзды:</b>"
                f" {repo_data.get('stargazers_count', 'N/A')}\n<b><emoji"
                " document_id=5361696340348779794>🪐</emoji>Форков:</b>"
                f" {repo_data.get('forks_count', 'N/A')}\n<b><emoji"
                " document_id=5334704798765686555>👀</emoji>Просмотревших:</b>"
                f" {repo_data.get('watchers_count', 'N/A')}\n"
            )
            if avatar_url := repo_data.get("avatar_url"):
                await utils.answer_file(
                    message,
                    avatar_url,
                    info_text,
                    link_preview=False,
                )
            else:
                await utils.answer(message, info_text)
        except Exception:
            await utils.answer(message, self.strings["repo_not_found"])
