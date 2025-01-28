# File: llm_setup.py
from crewai import LLM
import os

class LLMSetup:
    @staticmethod
    def get_llm():
        """Configure and return the LLM instance"""
        return LLM(
            model="gemini/gemini-2.0-flash-thinking-exp-01-21",
            temperature=0.7
        )