user_data = '''
/*
Selects all the data we need from the database

Its stores guild to guild

Makes warning systems easier to manage
*/
SELECT 
    (Strikes, Logged_In, Registered_At, Messages, Bot, Commands, Email, Password, Servers, Premium, LastUpdate, Admin, SupportBoosts)
FROM 
    "users" 
WHERE 
    UserID = ? AND GuildID = ? AND name LIKE %GuildID%
'''
