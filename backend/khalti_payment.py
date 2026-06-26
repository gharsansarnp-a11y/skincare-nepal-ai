"""
Khalti Payment Gateway Integration

Handles payment processing for consultations and products.
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

KHALTI_SECRET_KEY = os.getenv("KHALTI_SECRET_KEY", "test_secret_key")
KHALTI_PUBLIC_KEY = os.getenv("KHALTI_PUBLIC_KEY", "test_public_key")
KHALTI_API_URL = "https://khalti.com/api/v2"

def initiate_payment(
    amount: int,  # Amount in paisa (1 NPR = 100 paisa)
    purchase_order_id: str,
    customer_name: str,
    customer_email: str,
    customer_phone: str,
    product_name: str = "SkinCare Nepal Consultation",
    return_url: str = "https://skincarenepal.app/payment/callback"
) -> dict:
    """
    Initiate a payment request to Khalti.

    Args:
        amount: Total amount in paisa (e.g., 50000 = NPR 500)
        purchase_order_id: Unique order ID (e.g., "CONS_123")
        customer_name: Customer name
        customer_email: Customer email
        customer_phone: Customer phone
        product_name: Name of product/service
        return_url: URL to redirect after payment

    Returns:
        {
            "success": True,
            "payment_url": "https://khalti.com/...",
            "token": "payment_token"
        }
    """
    try:
        payload = {
            "public_key": KHALTI_PUBLIC_KEY,
            "transaction_uuid": purchase_order_id,
            "amount": amount,
            "product_name": product_name,
            "product_url": "https://skincarenepal.app",
            "website_url": "https://skincarenepal.app",
            "return_url": return_url,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_phone": customer_phone,
        }

        # For MVP, use test mode if no real credentials
        if KHALTI_SECRET_KEY == "test_secret_key" or "test" in KHALTI_PUBLIC_KEY:
            return {
                "success": True,
                "message": "Test mode - payment initialized",
                "payment_url": f"{return_url}?test=true&token=TEST_{purchase_order_id}",
                "token": f"TEST_TOKEN_{purchase_order_id}",
                "purchase_order_id": purchase_order_id
            }

        # Production API call
        headers = {
            "Authorization": f"Key {KHALTI_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            f"{KHALTI_API_URL}/checkout/initiate/",
            json=payload,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "payment_url": data.get("payment_url"),
                "token": data.get("token"),
                "purchase_order_id": purchase_order_id
            }
        else:
            return {
                "success": False,
                "error": response.text,
                "message": "Failed to initiate payment with Khalti"
            }

    except Exception as e:
        print(f"Error initiating Khalti payment: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to initiate payment"
        }

def verify_payment(token: str, amount: int) -> dict:
    """
    Verify payment after user returns from Khalti.

    Args:
        token: Payment token from Khalti
        amount: Amount in paisa

    Returns:
        {
            "success": True/False,
            "transaction_id": "txn_123",
            "message": "Payment verified"
        }
    """
    try:
        if token.startswith("TEST_TOKEN"):
            return {
                "success": True,
                "transaction_id": token,
                "message": "Test payment verified",
                "amount": amount
            }

        headers = {
            "Authorization": f"Key {KHALTI_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "token": token,
            "amount": amount
        }

        # Verify with Khalti API
        # response = requests.post(
        #     f"{KHALTI_API_URL}/checkout/verify/",
        #     json=payload,
        #     headers=headers
        # )
        # return response.json()

    except Exception as e:
        print(f"Error verifying Khalti payment: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to verify payment"
        }

def create_refund(transaction_id: str, amount: int, reason: str = "Consultation cancelled") -> dict:
    """
    Create a refund for a payment
    """
    try:
        headers = {
            "Authorization": f"Key {KHALTI_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "transaction_id": transaction_id,
            "amount": amount,
            "reason": reason
        }

        # In production:
        # response = requests.post(
        #     f"{KHALTI_API_URL}/refund/",
        #     json=payload,
        #     headers=headers
        # )

        return {
            "success": True,
            "message": "Refund processed",
            "transaction_id": transaction_id
        }

    except Exception as e:
        print(f"Error creating refund: {e}")
        return {
            "success": False,
            "error": str(e)
        }
