"""
Calculator tool for mathematical operations.
Evaluates mathematical expressions safely.
"""

import re
import math
from typing import Union


class CalculatorTool:
    """
    Calculator tool for mathematical operations.
    """

    ALLOWED_NAMES = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'sqrt': math.sqrt,
        'log': math.log,
        'exp': math.exp,
        'pi': math.pi,
        'e': math.e
    }

    @staticmethod
    def calculate(expression: str) -> Union[float, str]:
        """
        Evaluate a mathematical expression safely.

        Args:
            expression (str): Mathematical expression to evaluate.

        Returns:
            Union[float, str]: Result of the calculation or error message.
        """
        try:
            # Remove spaces
            expression = expression.replace(" ", "")

            # Check for dangerous patterns
            dangerous_patterns = ['__', 'import', 'exec', 'eval', 'open', 'file']
            for pattern in dangerous_patterns:
                if pattern in expression.lower():
                    return "Error: Unsafe expression"

            # Safely evaluate using restricted namespace
            result = eval(expression, {"__builtins__": {}}, CalculatorTool.ALLOWED_NAMES)
            return float(result)
        except ZeroDivisionError:
            return "Error: Division by zero"
        except ValueError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Error: Invalid expression - {str(e)}"

    @staticmethod
    def is_calculation_needed(user_input: str) -> bool:
        """Check if calculator tool is needed."""
        calc_keywords = ["calculate", "compute", "solve", "what is", "equals", "math", "+", "-", "*", "/"]
        return any(keyword in user_input.lower() for keyword in calc_keywords)
