css = """
<style>
/* Claude-themed Background */
body, .stApp {
    background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 50%, #E5E7EB 100%);
    min-height: 100vh;
}

/* Header Section - Claude Style */
.app-header {
    text-align: center;
    padding: 3rem 2rem 2rem;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    border-radius: 1rem;
    margin: 2rem auto 2rem;
    max-width: 900px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border: 1px solid rgba(255,255,255,0.2);
}

/* Logo Container */
.logo-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

/* Claude-inspired Logo Circle */
.app-logo {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #F59E0B 0%, #D97706 50%, #B45309 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 1.5rem;
    box-shadow: 0 4px 12px rgba(217, 119, 6, 0.3);
    position: relative;
}

.app-logo::after {
    content: '';
    position: absolute;
    inset: 2px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 100%);
    pointer-events: none;
}

/* Main Title - Claude Style */
.app-title {
    color: #1F2937;
    font-weight: 700;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    background: linear-gradient(135deg, #1F2937 0%, #374151 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Subtitle */
.app-subtitle {
    color: #6B7280;
    font-size: 1.1rem;
    font-weight: 400;
    margin-bottom: 1rem;
    opacity: 0.8;
}

/* Brand tagline */
.app-tagline {
    color: #D97706;
    font-size: 0.9rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 1rem;
}

/* Chat Container */
.chat-container {
    max-width: 800px;
    margin: 0 auto 2rem;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 1rem;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border: 1px solid rgba(255,255,255,0.2);
}

.chat-message {
    padding: 1.25rem 1.5rem;
    border-radius: 0.75rem;
    margin: 0.75rem 0;
    font-size: 0.95rem;
    line-height: 1.6;
    max-width: 85%;
    word-wrap: break-word;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    border: 1px solid transparent;
    transition: box-shadow 0.2s ease;
}

.chat-message:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.chat-message.user {
    align-self: flex-end;
    background-color: #E5E7EB;
    color: #1F2937;
    margin-left: auto;
    border: 1px solid #D1D5DB;
}

.chat-message.bot {
    align-self: flex-start;
    background-color: #F9FAFB;
    color: #1F2937;
    margin-right: auto;
    border: 1px solid #E5E7EB;
}

.chat-wrapper {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    body, .stApp {
        background: linear-gradient(135deg, #111827 0%, #1F2937 50%, #374151 100%);
    }
    
    .app-header {
        background: rgba(31, 41, 55, 0.8);
        border-color: rgba(75, 85, 99, 0.3);
    }
    
    .app-title {
        color: #F9FAFB;
        background: linear-gradient(135deg, #F9FAFB 0%, #E5E7EB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .app-subtitle {
        color: #9CA3AF;
    }
    
    .app-tagline {
        color: #F59E0B;
    }
    
    .chat-container {
        background: rgba(31, 41, 55, 0.9);
        border-color: rgba(75, 85, 99, 0.3);
    }
    
    .chat-message.user {
        background-color: #374151;
        color: #F9FAFB;
        border-color: #4B5563;
    }
    
    .chat-message.bot {
        background-color: #1F2937;
        color: #F9FAFB;
        border-color: #374151;
    }
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