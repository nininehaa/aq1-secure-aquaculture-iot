import hashlib
import hmac


SECRET_KEY = b"aq1-week5-secret-key"

original_message = b"sensor01|DO|6.8"
modified_message = b"sensor01|DO|1.0"

generated_hmac = hmac.new(
    SECRET_KEY,
    original_message,
    hashlib.sha256
).hexdigest()

print(f"Original message: {original_message.decode()}")
print(f"Generated HMAC: {generated_hmac}")

expected_hmac = hmac.new(
    SECRET_KEY,
    original_message,
    hashlib.sha256
).hexdigest()

if hmac.compare_digest(generated_hmac, expected_hmac):
    print("PASS: message integrity verified")
else:
    print("FAIL: message integrity check failed")

modified_hmac = hmac.new(
    SECRET_KEY,
    modified_message,
    hashlib.sha256
).hexdigest()

print(f"\nModified message: {modified_message.decode()}")

if hmac.compare_digest(generated_hmac, modified_hmac):
    print("PASS: message integrity verified")
else:
    print("FAIL: message integrity check failed")
