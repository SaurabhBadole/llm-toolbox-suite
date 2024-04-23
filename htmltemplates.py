css = '''
<style>
.chat-message {
    padding: 1.5rem; 
    border-radius: 0.5rem; 
    margin-bottom: 1rem; 
    display: flex;
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .message {
    width: 100%; /* Changed to 100% to fill the space previously occupied by the avatar */
    padding: 0 1.5rem;
    color: #fff;
}
</style>
'''

bot_template = '''
<!-- Bot Template -->
<div class="chat-message bot">
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<!-- User Template -->
<div class="chat-message user">
    <div class="message">{{MSG}}</div>
</div>
'''
