"""
VenomGuard - Standalone Chat Module (Backwards Compatibility Shim)
Delegates directly to function.llm_chat.only_chat.
"""

from function.llm_chat import only_chat, first_aid_chat, get_offline_medical_response

__all__ = ["only_chat", "first_aid_chat", "get_offline_medical_response"]
