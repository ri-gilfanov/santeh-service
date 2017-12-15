def delete_image_at_object_delete(sender, **kwargs):
    '''Удаление файла изображения при удалении объекта'''
    try:
        object_ = kwargs.get('instance')
        storage, path = object_.image.storage, object_.image.path
        storage.delete(path)
    except:
        pass


def delete_image_at_object_change(post_object):
    '''Удаление файла изображения при изменении объекта'''
    try:
        pre_object = post_object.__class__.objects.get(id=post_object.id)
        if pre_object.image != post_object.image:
            pre_object.image.delete(save=False)
    except:
        pass
