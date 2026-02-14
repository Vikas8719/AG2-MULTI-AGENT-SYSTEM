"""Agent tests"""
import pytest
from agents import AnalyzerAgent
from config import settings

def test_analyzer_agent():
    agent = AnalyzerAgent(settings)
    assert agent.name == "AnalyzerAgent"
    assert agent.state['status'] == 'initialized'
