# File: llm_setup.py
from crewai import LLM
import os

class LLMSetup:
    @staticmethod
    def get_llm():
        """Configure and return the LLM instance"""
        return LLM(
            model="groq/llama-3.3-70b-versatile",
            temperature=0.7
        )
