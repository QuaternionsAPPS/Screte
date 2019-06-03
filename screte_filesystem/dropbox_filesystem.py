import dropbox
from screte_filesystem.dropbox_token import token


dbx = dropbox.Dropbox(token)


def upload_image(img_str, id):
    dbx.files_upload(img_str, "/{}.jpg".format(id))


def download_image(id, path):
    image_name = '{}.jpg'.format(id)
    r = dbx.files_download_to_file('{}{}'.format(path, image_name), '/{}'.format(image_name))
