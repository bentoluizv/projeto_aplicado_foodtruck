from supabase import Client


def list_all_icons(
    supabase: Client,
    limit: int = 100,
    offset: int = 0,
    sort_by={'column': 'name', 'order': 'desc'},
):
    """
    Retrieves a list of all files in the 'category-icons' bucket, with pagination and sorting options.

    Args:
        limit (int, optional): The maximum number of files to retrieve. Defaults to 100.
        offset (int, optional): The number of files to skip before starting to retrieve. Defaults to 0.
        sort_by (dict, optional): A dictionary specifying the sorting options. It should contain:
            - 'column' (str): The column to sort by (e.g., 'name').
            - 'order' (str): The sorting order ('asc' for ascending, 'desc' for descending).
            - Defaults to {'column': 'name', 'order': 'desc'}.

    Returns:
        list: A list of dictionaries, where each dictionary represents a file and contains:
            - 'id' (str): The unique identifier extracted from the file name.
            - 'icon' (str): The name of the icon extracted from the file name.
            - 'url' (str): The public URL of the file.

    Raises:
        Exception: If there is an issue with retrieving files or generating public URLs.

    Note:
        The function assumes that file names in the bucket follow the format 'name_id'.
        Ensure that the Supabase client is properly initialized and authenticated before calling this function.
    """  # noqa: E501

    bucket_name = 'category-icons'
    files = supabase.storage.from_(bucket_name).list(
        options={
            'limit': limit,
            'offset': offset,
            'sortBy': sort_by,
        },
    )
    result = []

    for file in files:
        file_name = file['name']

        if file_name.startswith('add_'):
            continue

        public_url = supabase.storage.from_(bucket_name).get_public_url(
            file_name
        )
        name, id = file_name.replace('.png', '').split('_')

        result.append({'id': id, 'icon': name, 'url': public_url})

    return {'icons': result}


def uploadProductImage(supabase: Client, image: bytes, file_name: str) -> str:  # noqa: E501
    """
    Uploads a product image to the Supabase storage bucket.

    Returns:
        str: The public URL of the uploaded image.

    Raises:
        Exception: If there is an issue with uploading the image or generating the public URL.
    """  # noqa: E501

    bucket_name = 'product-images'

    storage = supabase.storage

    res = storage.from_(bucket_name).upload(
        file=image, path=f'{file_name}.png'
    )

    public_url = storage.from_(bucket_name).get_public_url(res.path)

    return public_url
