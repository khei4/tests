import dropbox
import os

DROPBOX_ACCESS_TOKEN = os.environ.get("DROPBOX_ACCESS_TOKEN")

dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)


try:
    files = dbx.files_list_folder("")
    links = []
    for entry in files.entries:
        if isinstance(entry, dropbox.files.FileMetadata):
            # 共有リンクを取得または作成
            try:
                shared_link_metadata = dbx.sharing_create_shared_link_with_settings(
                    entry.path_lower
                )
                link = shared_link_metadata.url
            except dropbox.exceptions.ApiError as err:
                if err.error.is_shared_link_already_exists():
                    shared_links = dbx.sharing_list_shared_links(
                        path=entry.path_lower
                    ).links
                    if shared_links:
                        link = shared_links[0].url
                else:
                    print(f"共有リンクの取得に失敗しました。エラー: {err}")
                    continue
            # change it to download link
            link = link.replace("www.dropbox.com", "dl.dropboxusercontent.com")
            link = link.replace("&dl=0", "")
            links.append((entry, link))

    # sorted_links = sorted(links, key=lambda x: x[0].client_modified, reverse=True)
    sorted_links = sorted(links, key=lambda x: x[0].name, reverse=True)

    for entry, link in sorted_links:
        print(
            f"ファイル名: {entry.name}, アップロード日時: {entry.client_modified}, リンク: {link}"
        )
except dropbox.exceptions.ApiError as err:
    print(f"フォルダ一覧の取得に失敗しました。エラー: {err}")
