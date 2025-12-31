===FILE===
runs/rule_service.py
class RuleService:
    def __init__(self, rules):
        self.rules = rules

    def evaluate(self, transaction):
        matched_rules = []
        for rule in self.rules:
            if self.evaluate_rule(rule, transaction):
                matched_rules.append(rule)
                if rule['action'] == 'DECLINE':
                    return {'decision': 'DECLINE', 'matched_rules': matched_rules}
        return {'decision': 'APPROVE', 'matched_rules': matched_rules}

    def evaluate_rule(self, rule, transaction):
        condition = rule['condition']
        try:
            return eval(condition, {}, transaction)
        except Exception as e:
            return False
        

===FILE===
runs/test_rule_service.py
import unittest
from rule_service import RuleService

class TestRuleService(unittest.TestCase):
    def setUp(self):
        self.rules = [
            {'rule_id': '2', 'category': 'Stolen Card', 'use_case': 'Multiple transactions in short time window', 'primary_feature': 'txn_count_5m', 'secondary_feature': 'same_amount_repeat', 'condition': 'txn_count_5m > 3', 'threshold': '', 'time_window': '5m', 'action': 'DECLINE', 'criticality': 'High'},
            {'rule_id': '3', 'category': 'Stolen Card', 'use_case': 'First transaction after long inactivity', 'primary_feature': 'new_merchant_flag', 'secondary_feature': 'merchant_risk_score', 'condition': 'new_merchant_flag == True', 'threshold': 'medium', 'time_window': '', 'action': 'STEP_UP', 'criticality': 'Medium'},
            {'rule_id': '4', 'category': 'Stolen Card', 'use_case': 'Transaction from unusual merchant', 'primary_feature': 'offline_txn_flag', 'secondary_feature': 'entry_mode', 'condition': 'offline_txn_flag == True', 'threshold': '', 'time_window': '', 'action': 'DECLINE', 'criticality': 'High'},
            {'rule_id': '5', 'category': 'Stolen Card', 'use_case': 'High-value purchase after theft', 'primary_feature': 'amount_spike_ratio', 'secondary_feature': 'avg_amount_30d', 'condition': 'amount_spike_ratio > 2', 'threshold': '', 'time_window': '', 'action': 'DECLINE', 'criticality': 'High'},
            # Add more rules as needed for testing
        ]
        self.service = RuleService(self.rules)

    def test_decline_due_to_multiple_transactions(self):
        transaction = {'txn_count_5m': 4, 'same_amount_repeat': 1}
        result = self.service.evaluate(transaction)
        self.assertEqual(result['decision'], 'DECLINE')
        self.assertEqual(len(result['matched_rules']), 1)
        self.assertEqual(result['matched_rules'][0]['rule_id'], '2')

    def test_step_up_due_to_new_merchant(self):
        transaction = {'new_merchant_flag': True, 'merchant_risk_score': 'medium'}
        result = self.service.evaluate(transaction)
        self.assertEqual(result['decision'], 'APPROVE')
        self.assertEqual(len(result['matched_rules']), 1)
        self.assertEqual(result['matched_rules'][0]['rule_id'], '3')

    def test_decline_due_to_offline_transaction(self):
        transaction = {'offline_txn_flag': True, 'entry_mode': 'card'}
        result = self.service.evaluate(transaction)
        self.assertEqual(result['decision'], 'DECLINE')
        self.assertEqual(len(result['matched_rules']), 1)
        self.assertEqual(result['matched_rules'][0]['rule_id'], '4')

    def test_decline_due_to_high_value_purchase(self):
        transaction = {'amount_spike_ratio': 3, 'avg_amount_30d': 100}
        result = self.service.evaluate(transaction)
        self.assertEqual(result['decision'], 'DECLINE')
        self.assertEqual(len(result['matched_rules']), 1)
        self.assertEqual(result['matched_rules'][0]['rule_id'], '5')

    # Add more tests to cover all FEATURE_MAP combinations

if __name__ == '__main__':
    unittest.main()