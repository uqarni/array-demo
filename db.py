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

    if session_state.industry == "Solar":
        initial_text = "{lead_first_name},\n\nToo many unqualified leads or chargebacks?\n\nWe can solve that in an eligibility workflow.\n\nOur credit tools help solar partners determine consumer eligibility, reducing the number of disqualified leads and chargebacks.\n\nCurious to learn how we do it?"
    elif session_state.industry == "Telecom/Energy/Utilities":
        initial_text = "Hey {lead_first_name},\n\nWhat are you currently doing to combat late payments / delinquencies?\n\nWe help organizations like yours assess customer credit during the enrollment process to reduce your risk.\n\nOur model can help determine which customers should require a security deposit based on their credit profile. Any interest?"
    elif session_state.industry == "Lead Generators":
        initial_text = "Hey {lead_first_name},\n\nAre you looking at credit data for new leads?\n\nOur credit technology provides insight into your consumer's credit profile - making it easy to prioritize leads, lower marketing costs, and drive conversions."
    elif session_state.industry == 'Insurance':
         initial_text = "{lead_first_name} - \n\nAt Array, we help insurance companies like yours better engage and understand their customers.\n\nWe have hundreds of partners leveraging our consumer-facing tools and back-end data layer today.\n\nWould increasing your consumer engagement be worth a conversation?\n\nLet me know if this sounds relevant, would love to chat.'
    elif session_state.industry == "Mortgage":
        initial_text = "Hi {lead_first_name},\n\nMortgage companies are using Array's platform to:\n\n-determine consumer eligibility\n\n-prioritize borrowers for mortgage or refi products and\n\n-increase conversion rates\n\nCurious how {company_name} could leverage consumer level credit data?"
    elif session_state.industry == "Home Services":
        initial_text = "{lead_first_name},\n\nToo many unqualified leads or chargebacks?\n\nWe can solve that in an eligibility workflow.\n\nOur credit tools help home services organizations like yours determine consumer eligibility, reducing the number of disqualified leads and chargebacks.\n\nCurious to learn how we do it?"
    
    session_state.initial_text = initial_text
    session_state.messages.insert(0, {'role': 'assistant', 'content': initial_text})
