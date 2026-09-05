import unittest
from pathlib import Path

from changebench.engine import ScenarioError, evaluate, load_json
from changebench.report import markdown


ROOT = Path(__file__).parents[1]


class ChangeBenchTests(unittest.TestCase):
    def setUp(self):
        self.scenario = load_json(ROOT / "scenarios/azure-private-dns-outage.json")
        self.proposal = load_json(ROOT / "examples/reference-proposal.json")

    def test_reference_passes_and_is_deterministic(self):
        first = evaluate(self.scenario, self.proposal)
        second = evaluate(self.scenario, self.proposal)
        self.assertTrue(first.passed)
        self.assertEqual(first.score, 100)
        self.assertEqual(first.receipt, second.receipt)

    def test_boundary_violation_is_hard_failure(self):
        self.proposal["actions"].append("delete_resource_group")
        self.assertFalse(evaluate(self.scenario, self.proposal).passed)

    def test_missing_contract_is_rejected(self):
        with self.assertRaisesRegex(ScenarioError, "rollback"):
            evaluate(self.scenario, {"agent_name": "bad", "actions": [], "evidence": []})

    def test_receipt_changes_with_result(self):
        original = evaluate(self.scenario, self.proposal).receipt
        self.proposal["tool_calls"] = 8
        self.assertNotEqual(evaluate(self.scenario, self.proposal).receipt, original)

    def test_report_contains_decision_and_economics(self):
        report = markdown(evaluate(self.scenario, self.proposal))
        self.assertIn("**Decision:** PASS", report)
        self.assertIn("Unit economics", report)

    def test_every_shipped_scenario_has_a_passing_reference(self):
        pairs = {
            "azure-private-dns-outage.json": "reference-proposal.json",
            "kubernetes-gpu-rightsizing.json": "kubernetes-gpu-proposal.json",
            "bgp-route-leak.json": "bgp-route-leak-proposal.json",
        }
        for scenario_name, proposal_name in pairs.items():
            with self.subTest(scenario=scenario_name):
                result = evaluate(
                    load_json(ROOT / "scenarios" / scenario_name),
                    load_json(ROOT / "examples" / proposal_name),
                )
                self.assertTrue(result.passed)
                self.assertEqual(result.score, 100)


if __name__ == "__main__":
    unittest.main()
