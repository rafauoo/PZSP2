import magic


def is_allowed_file_type(file_content):
    allowed_types = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'image/jpeg',
        'image/png',
    ]

    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file_content)
    return file_type in allowed_types
