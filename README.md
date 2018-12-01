# BookmarkMe bot
A GroupMe chatbot that allows you to bookmark messages for future reference. It is a simple Flask app deployed to Heroku and uses MongoDB for saving bookmarks.

## Usage
The bot supports the following commands. These descriptions follow the default command names but you can customize them when you deploy the bot. You run these "commands" just by sending them as messages in the chat.
### Bookmark a message
The `:save` command allows you to save/bookmark messages. Probably the most important command.
- `:save` will try to save the last message that was "stored". The bot stores every message that was sent in the group for the next 24 hours (after which the messages are deleted). When the bot is newly added to the chat, it has no messages to store.
- `:save <text>` will find the last stored message that contains the specified text. For example, if "IMPORTANT MESSAGE" was the text of the message previously sent, then typing `:save IMPORTANT` should be enough to bookmark it.
- `:save "<text>"` will store the text between the double quotes verbatim. For example, typing `:save "MORE IMPORTANT MESSAGE"` will bookmark "MORE IMPORTANT MESSAGE".
### View a bookmark
You can view all saved bookmarks by typing `:all` but that would spam the group, so you can use the `:show` command.
- `:show` will try to display the most recently saved bookmark.
- `:show <text>` will display the bookmark containing the specified text. For example, typing `:show IMPORTANT` after storing the two examples above will display "MORE IMPORTANT MESSAGE"
### Delete a bookmark
If you don't need a bookmark anymore, you can delete it by using `:delete <text>` following a similar format to the examples above.

## Add the BookmarkMe bot to your own chat
There are a few simple steps involved here.
1. Deploy the app to Heroku using the button below. Give it a memorable name; we will need it later.

    [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
2. Create a bot user at the [GroupMe dev site](https://dev.groupme.com/bots). Assign it to the chat you want to add it, give it a name and an [optional] avatar, and for the callback URL, use **https://`<name>`.herokuapp.com** where `<name>` corresponds to the name you used in step #1.
3. Now copy the "bot ID" field on the GroupMe dev site.
4. Go to your app dashboard on Heroku (clicking "Manage" when the install finishes in step #1) and in the settings tab, change the config variable `BOT_ID` from default to the value you copied in step #3.
5. (Optional) You can change the default values of the other variables in the list. `BOT_NAME` is the name of the bot, and the others are commands to trigger the bot.
6. Once you're done creating the Heroku instance, you should be good to go. Note that you will need a credit card attached to your account to deploy the database, but since it uses the free plan, there will never be any charge.
