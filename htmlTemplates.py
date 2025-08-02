css = """
<style>
.chat-container {
    max-width: 800px;
    margin: 2rem auto;
    font-family: 'Helvetica Neue', sans-serif;
}

.chat-message {
    padding: 1rem 1.5rem;
    border-radius: 1rem;
    margin: 0.5rem 0;
    font-size: 0.95rem;
    line-height: 1.6;
    max-width: 90%;
    word-wrap: break-word;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

.chat-message.user {
    align-self: flex-end;
    background-color: #fff7e0;
    color: #333;
    margin-left: auto;
}

.chat-message.bot {
    align-self: flex-start;
    background-color: #f1f3f4;
    color: #111;
    margin-right: auto;
}

.chat-wrapper {
    display: flex;
    flex-direction: column;
}
</style>
"""

bot_template = """
<div class="chat-wrapper">
    <div class="chat-message bot">
        {{MSG}}
    </div>
</div>
"""

user_template = """
<div class="chat-wrapper">
    <div class="chat-message user">
        {{MSG}}
    </div>
</div>
"""
