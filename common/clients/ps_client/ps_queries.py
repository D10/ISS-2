GET_USER_BY_ID = """
    SELECT
        id,
        name,
        access_key
    FROM users
    WHERE id=%d;
"""

GET_USER_BY_ACCESS_KEY = """
    SELECT
        id,
        name,
        auth_key
    FROM users
    WHERE auth_key='%s'
"""

GET_ROUTER_CONFIG = """
    SELECT
        ic.id,
        ic.slack_integration,
        ic.rocket_integration,
        ic.telegram_integration,
        si.token as slack_token,
        ti.token as telegram_token,
        ti.chat_id as telegram_chat_id,
        ri.login as rocket_login,
        ri.password as rocket_password
    FROM integrations_config ic
        LEFT JOIN slack_integration si
            ON ic.id = si.config_id
        LEFT JOIN telegram_integration ti
            ON ic.id = ti.config_id
        LEFT JOIN rocket_integration ri
            ON ic.id = ri.config_id
    WHERE ic.id=%d;
"""
