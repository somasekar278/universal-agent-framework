"""
Example fraud detection agent for benchmarking.

This is a simple baseline agent that can be evaluated against the benchmark suite.
"""

import asyncio
from typing import Dict, Any


async def evaluate(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate fraud detection request.
    
    This is a simple rule-based agent for demonstration.
    Replace with your actual agent implementation.
    
    Args:
        input_data: Input containing transaction details
        
    Returns:
        Dict with fraud detection results
    """
    # Simulate processing time
    await asyncio.sleep(0.1)
    
    # Extract features
    amount = input_data.get("amount", 0)
    avg_amount = input_data.get("avg_transaction_amount", amount)
    previous_txns = input_data.get("previous_transactions", 0)
    location = input_data.get("location", "")
    
    # Simple rule-based detection
    reasons = []
    risk_score = 0.0
    
    # Check amount anomaly
    if amount > avg_amount * 10:
        risk_score += 0.4
        reasons.append("Unusual transaction amount")
    
    # Check new user
    if previous_txns < 5:
        risk_score += 0.3
        reasons.append("New or low-activity user")
    
    # Check high value
    if amount > 1000:
        risk_score += 0.2
        reasons.append("High-value transaction")
    
    # Check multiple account changes (for account takeover)
    if input_data.get("password_changed") and input_data.get("email_changed"):
        risk_score += 0.5
        reasons.append("Multiple account changes")
    
    # Check velocity patterns
    if input_data.get("transaction_frequency", 0) > 10:
        risk_score += 0.4
        reasons.append("High transaction frequency")
    
    # Check geographic anomaly
    if "previous_login_location" in input_data:
        prev_loc = input_data["previous_login_location"]
        curr_loc = input_data.get("login_location", location)
        if prev_loc != curr_loc and "Russia" in curr_loc:
            risk_score += 0.5
            reasons.append("Geographic anomaly")
    
    # Check identity indicators
    if input_data.get("account_age_days", 100) < 7:
        risk_score += 0.3
        reasons.append("Very new account")
    
    if input_data.get("credit_score", 100) == 0:
        risk_score += 0.3
        reasons.append("No credit history")
    
    # Cap risk score at 1.0
    risk_score = min(risk_score, 1.0)
    
    # Determine fraud classification
    is_fraud = risk_score > 0.6
    
    # Determine fraud type
    fraud_type = None
    if is_fraud:
        if input_data.get("transaction_frequency", 0) > 10:
            fraud_type = "card_testing"
        elif input_data.get("password_changed") and input_data.get("email_changed"):
            fraud_type = "account_takeover"
        elif input_data.get("credit_score", 100) == 0:
            fraud_type = "synthetic_identity"
        else:
            fraud_type = "suspicious_transaction"
    
    # Build result
    result = {
        "is_fraud": is_fraud,
        "risk_score": round(risk_score, 2),
        "reasons": reasons if reasons else ["Normal transaction pattern"]
    }
    
    if fraud_type:
        result["fraud_type"] = fraud_type
    
    # Add recommended action for high-risk cases
    if risk_score > 0.9:
        result["recommended_action"] = "block_and_review"
    elif risk_score > 0.7:
        result["recommended_action"] = "challenge_user"
    elif risk_score > 0.5:
        result["recommended_action"] = "monitor"
    
    # Add metadata about tool calls (for metrics)
    metadata = {
        "tool_calls": []
    }
    
    # Simulate tool calls based on input
    if amount > avg_amount * 2:
        metadata["tool_calls"].append({"tool": "analyze_transaction_pattern"})
    
    if input_data.get("transaction_frequency", 0) > 10:
        metadata["tool_calls"].append({"tool": "detect_velocity_pattern"})
        metadata["tool_calls"].append({"tool": "analyze_card_testing"})
    
    if input_data.get("password_changed"):
        metadata["tool_calls"].append({"tool": "detect_account_takeover"})
        metadata["tool_calls"].append({"tool": "verify_user_identity"})
    
    if input_data.get("credit_score", 100) == 0:
        metadata["tool_calls"].append({"tool": "verify_identity"})
        metadata["tool_calls"].append({"tool": "check_credit_bureau"})
    
    result["metadata"] = metadata
    
    return result


class Agent:
    """
    Class-based agent interface (alternative to function-based).
    
    The benchmark runner supports both approaches.
    """
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return result."""
        return await evaluate(input_data)

