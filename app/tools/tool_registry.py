"""
Registry for KnowledgeMind tools.
"""

from app.tools.calculator_tool import CalculatorTool


class ToolRegistry:

    def __init__(self):

        self.calculator = CalculatorTool()