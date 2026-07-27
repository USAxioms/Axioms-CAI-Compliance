"""
Weak Arithmetic Decidability (WAD) Python Wrapper
------------------------------------------------
Pure Python orchestration layer wrapping the WAD engine, rule parsing, 
and invariant verification with zero external dependencies.
"""

import json
from typing import Dict, Any, Optional
from src.core.wad_engine import WADEngine, Constant, Variable, Add, LessEqual, And, Exists
from safety.omega_protocol import OmegaProtocolEnforcer

class WADPythonWrapper:
    """
    Encapsulates the Weak Arithmetic Decidability engine and rule execution 
    entirely within a Python execution context.
    """
    def __init__(self, rules_path: str = "rules/compliance_rules.json"):
        self.engine = WADEngine()
        self.enforcer = OmegaProtocolEnforcer()
        self.rules = self._load_rules(rules_path)

    def _load_rules(self, path: str) -> Dict[str, Any]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback inline default ruleset if file is missing
            return {
                "framework": "Axiomatic-Ontological-Intelligence",
                "ruleset_id": "CAI-COMPLIANCE-01"
            }

    def execute_evaluation(self, environment: Dict[str, int]) -> Dict[str, Any]:
        # Construct the core WAD AST constraint check
        ast = Exists(
            variable="y",
            domain_start=0,
            domain_stop=15,
            domain_step=1,
            formula=And(
                LessEqual(
                    Add(Variable("x"), Variable("y")),
                    Constant(20)
                ),
                LessEqual(
                    Constant(0),
                    Variable("y")
                )
            )
        )

        # Evaluate via WAD engine
        is_satisfied = self.engine.evaluate(ast, environment)
        receipt = self.engine.generate_receipt(ast, "SATISFIABLE" if is_satisfied else "UNSATISFIABLE")

        # Enforce safety invariants through Omega protocol
        self.enforcer.verify_invariant(receipt)

        return {
            "evaluation_result": is_satisfied,
            "compliance_receipt": receipt,
            "ruleset_metadata": self.rules
        }


if __name__ == "__main__":
    wrapper = WADPythonWrapper()
    result = wrapper.execute_evaluation({"x": 5})
    print("WAD Python Wrapper Execution Success:")
    print(json.dumps(result, indent=2))

