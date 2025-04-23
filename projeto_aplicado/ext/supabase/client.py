from projeto_aplicado.settings import get_settings
from supabase import Client, ClientOptions, create_client

settings = get_settings()

options = ClientOptions(
    auto_refresh_token=True,
    postgrest_client_timeout=10,
    storage_client_timeout=10,
    schema='public',
)

supabase: Client = create_client(
    settings.SUPABASE_URL, settings.SUPABASE_SERVICE_SECRET, options
)


def get_supabase_client() -> Client:
    """
    Returns the Supabase client instance.
    """
    return supabase
