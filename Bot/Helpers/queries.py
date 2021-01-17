user_data = '''
SELECT 
    (Strikes, Logged_In, Registered_At, Messages, Bot, Commands, Email, Password, Servers, Premium, LastUpdate, Admin, SupportBoosts)
FROM 
    "users" 
WHERE 
    UserID = ? AND GuildID = ? AND name LIKE %GuildID%
'''

warns = '''
SELECT
    *
FROM
    "warns"
WHERE
    UserID = ? AND GuildID = ? AND name LIKE %warn%
'''

starboard = '''
SELECT
    *
FROM
    "starboard"
WHERE
    GuildID = ?
'''
