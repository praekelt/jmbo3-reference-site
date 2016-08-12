# 1. Confirm the authentication works.
# 2. Create an admin user, non-staff user, two ModelBase objects in the tests. One published, the other not.
# 3. Confirm admin has access to all, non-staff only has access to published.
# 4. You only need to test retrieval because other API functions are already tested in DRF, DRFE and Jmbo.