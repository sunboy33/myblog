from qiniu import Auth, BucketManager


def get_qiniu_file_urls(access_key, secret_key, bucket_name, folder_path, domain):
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)
    file_urls = []
    marker = None

    while True:
        ret, eof, info = bucket.list(bucket_name, prefix=folder_path, marker=marker)
        if ret is None:
            break
        for item in ret.get('items', []):
            file_key = item['key']
            if file_key == folder_path:
                continue
            file_urls.append(f'{domain}{file_key}')
        if eof:
            break
        marker = ret.get('marker')

    return file_urls


def upload_to_qiniu(file_path, file_data, old_src_path=None):
    from qiniu import Auth, put_data, BucketManager
    from django.conf import settings

    auth = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
    token = auth.upload_token(settings.QINIU_BUCKET_NAME, file_path)
    bucket = BucketManager(auth)

    try:
        _, info = put_data(token, file_path, file_data.read())
        if info.status_code != 200:
            return False, "上传失败"

        if old_src_path and not old_src_path.endswith('default.png'):
            old_key = old_src_path.replace(settings.QINIU_DOMAIN_URL + '/', '')
            try:
                bucket.delete(bucket=settings.QINIU_BUCKET_NAME, key=old_key)
            except Exception:
                pass

        return True, f"{settings.QINIU_DOMAIN_URL}/{file_path}"

    except Exception as e:
        return False, str(e)


def delete_from_qiniu(file_url):
    from qiniu import Auth, BucketManager
    from django.conf import settings

    auth = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
    bucket = BucketManager(auth)
    key = file_url.replace(settings.QINIU_DOMAIN_URL + '/', '')
    try:
        bucket.delete(settings.QINIU_BUCKET_NAME, key)
        return True
    except Exception:
        return False
