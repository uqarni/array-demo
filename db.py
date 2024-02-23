from supabase import create_client, Client
import os

def initialize_prompt_and_text(session_state):
    #connect to supabase database
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")

    supabase: Client = create_client(url, key)
    data, count = supabase.table("bots_dev").select("*").eq("id", "aria").execute()
    bot_info = data[1][0]

    system_prompt = bot_info['system_prompt']
    initial_text = bot_info['initial_text']
    to_format = {
        'lead_first_name': session_state.lead_first_name,
        'agent_name': 'Aria',
        'company_name': session_state.company_name,
        'mobile_vendor': session_state.mobile_vendor,
        "bank_or_credit_union": session_state.bank_or_credit_union,
        "customer_type": session_state.customer_type,
        'booking_link': 'array_booking.com'
    }
    initial_text = initial_text.format(**to_format)
    system_prompt = system_prompt.format(**to_format)

    session_state.system_prompt = system_prompt
    session_state.initial_text = initial_text
    session_state.messages.insert(0, {'role': 'assistant', 'content': initial_text})
