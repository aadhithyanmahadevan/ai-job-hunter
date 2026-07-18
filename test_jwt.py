from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)

access = create_access_token(
    {"sub": "test@example.com"}
)

refresh = create_refresh_token(
    {"sub": "test@example.com"}
)

print("\nACCESS TOKEN\n")
print(access)

print("\nREFRESH TOKEN\n")
print(refresh)

print("\nDECODED ACCESS TOKEN\n")
print(decode_token(access))