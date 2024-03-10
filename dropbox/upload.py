import argparse
import dropbox
import os

DROPBOX_ACCESS_TOKEN = os.environ.get("DROPBOX_ACCESS_TOKEN")

dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)


def upload_file(dropbox_path, local_path):
    """
    ローカルファイルをDropboxにアップロードする

    :param dropbox_path: Dropbox内のファイルの保存先パス
    :param local_path: アップロードするローカルファイルのパス
    """
    with open(local_path, "rb") as f:
        dbx.files_upload(f.read(), dropbox_path, mute=True)
    print(f"アップロード完了: {dropbox_path}")


def get_shared_link(dropbox_path):
    """
    Dropbox内のファイルの共有リンクを取得する

    :param dropbox_path: Dropbox内のファイルのパス
    :return: 共有リンクのURL
    """
    try:
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(
            dropbox_path
        )
        return shared_link_metadata.url
    except dropbox.exceptions.ApiError as err:
        if err.error.is_shared_link_already_exists():
            # 既に共有リンクが存在する場合はそれを取得
            result = dbx.sharing_list_shared_links(path=dropbox_path).links
            if result:
                return result[0].url
        print(f"共有リンクの取得に失敗しました。エラー: {err}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload a file to Dropbox and retrieve its shared link."
    )
    parser.add_argument(
        "local_file_path", type=str, help="The path to the local file to upload."
    )
    args = parser.parse_args()

    # Dropbox内の保存先パスをローカルファイル名に基づいて設定
    dropbox_file_path = f"/{os.path.basename(args.local_file_path)}"

    # ファイルをアップロード
    upload_file(dropbox_file_path, args.local_file_path)

    # 共有リンクを取得
    link = get_shared_link(dropbox_file_path)
    if link:
        print(f"共有リンク: {link}")
