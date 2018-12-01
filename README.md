# BookmarkMe bot
A GroupMe chatbot that allows you to bookmark messages

### Use the BookmarkMe bot in your own chat
There are a few simple steps involved here.
1. Deploy the app to Heroku using the button below. Give it a memorable name; we will need it later.

    [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
2. Create a bot user at the [GroupMe dev site](https://dev.groupme.com/bots). Assign it to the chat you want to add it, give it a name and an [optional] avatar, and for the callback URL, use **https://`<name>`.herokuapp.com** where `<name>` corresponds to the name you used in step #1.
3. Now copy the "bot ID" field on the GroupMe dev site.
4. Go to your app dashboard on Heroku (clicking "Manage" when the install finishes in step #1) and in the settings tab, change the config variable `BOT_ID` from default to the value you copied in step #3.
5. (Optional) You can change the default values of the other variables in the list. `BOT_NAME` is the name of the bot, and the others are commands to trigger the bot.
6. Once you're done creating the Heroku instance, you should be good to go. Note that you will need a credit card attached to your account to deploy the database, but since it uses the free plan, there will never be any charge.
