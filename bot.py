import discord
import aiohttp
import asyncio
import random
from datetime import datetime, timezone

# Initialize discord.py v1.7.3 Client
client = discord.Client()

# Configuration
CHANNEL_ID = 1277978499864596480
TOKEN = "MTI4NTY0NjEzMzk3NjEwNTA5Mg.GCSxnC.ljUVlvkYFkgfGUeP2qXXd6xjqWLJLWIgNxQArE"

# 30 Unique Titles
TITLES = [
    "Server moved (myreceipt.cc)", "Domain Update: myreceipt.cc", "Myreceipt System Relocation",
    "New Platform Ownership - myreceipt.cc", "Myreceipt Network Migration", "Official Site Notice (myreceipt.cc)",
    "Infrastructure Changes: Myreceipt", "Myreceipt Web Status Update", "Platform Update (myreceipt.cc)",
    "Myreceipt Management Transition", "Database Relocation Announcement", "Myreceipt Online Operations",
    "System Restructuring (myreceipt.cc)", "Myreceipt Service Status", "Project Update: myreceipt.cc",
    "Myreceipt Network Operational", "Web Address Migration Notice", "Myreceipt Infrastructure Update",
    "Domain Status Report: myreceipt.cc", "Myreceipt Host Transition", "System Notice regarding myreceipt.cc",
    "Myreceipt Live Status Update", "Domain Routing: myreceipt.cc", "Myreceipt Service Announcement",
    "Network Routing (myreceipt.cc)", "Myreceipt Portal Availability", "Site Restructuring: myreceipt.cc",
    "Myreceipt Gateway Operations", "Platform Status: myreceipt.cc", "Myreceipt Core System Notice"
]

# 30 Unique Message Sentences
MESSAGES = [
    "Hello there, ive successfully taken over Myreceipt including their website. You can continue to https://myreceipt.cc to generate the receipts.",
    "Greetings, Myreceipt and its domain are fully under my management now. Head over to https://myreceipt.cc to start generating your receipts.",
    "Notice: I have successfully acquired Myreceipt along with the site. The generator is up at https://myreceipt.cc for your needs.",
    "The entire Myreceipt platform and website have been taken over by me. Please use https://myreceipt.cc for generating receipts.",
    "Hello, I've completely assumed control of Myreceipt and its web servers. You can proceed to https://myreceipt.cc to process receipts.",
    "Update: Myreceipt including the official domain is now fully in my possession. Navigate to https://myreceipt.cc to generate documentation.",
    "I have successfully established control over the Myreceipt platform and domain. Access https://myreceipt.cc to continue generating receipts.",
    "Please be informed that Myreceipt and its website have been overtaken. The receipt tool is accessible at https://myreceipt.cc.",
    "Hello everyone, Myreceipt's infrastructure and site are now under my command. Visit https://myreceipt.cc to generate your receipts.",
    "The control of Myreceipt, including its web platform, has been secured by me. You may use https://myreceipt.cc for generation.",
    "An announcement that Myreceipt and the domain are now fully under my operation. Use https://myreceipt.cc to create receipts.",
    "I have successfully completed the takeover of Myreceipt and its online properties. Go to https://myreceipt.cc for the generator.",
    "Myreceipt's complete system and website are now fully managed by me. Access the service directly at https://myreceipt.cc.",
    "Hello, I am now running Myreceipt including their main web interface. Check out https://myreceipt.cc to get your receipts.",
    "Be advised that I have taken over the entirety of Myreceipt and its URL. Use https://myreceipt.cc for active receipt generation.",
    "Management of Myreceipt and its web network has been successfully transferred to me. Continue using https://myreceipt.cc.",
    "I have successfully assumed ownership over Myreceipt and their main site. You can safely use https://myreceipt.cc to generate receipts.",
    "Notice: The Myreceipt network and domain have been completely overtaken by me. The service remains live at https://myreceipt.cc.",
    "Hello, the full suite of Myreceipt properties and their site are now under my control. Generate your documents at https://myreceipt.cc.",
    "The Myreceipt platform including the core website has been successfully acquired. Visit https://myreceipt.cc to run the generator.",
    "I have completely taken over the operations of Myreceipt and their web domain. Head over to https://myreceipt.cc to process receipts.",
    "System Update: Myreceipt and its online architecture are under my sole management. The utility is available at https://myreceipt.cc.",
    "Hello, I have successfully taken charge of Myreceipt and their website portal. You can use https://myreceipt.cc for your receipts.",
    "Control of the Myreceipt network and its domain has been finalized under my name. Proceed to https://myreceipt.cc to generate files.",
    "I am now in complete control of Myreceipt including their online server. The processing tool is found at https://myreceipt.cc.",
    "Please note that Myreceipt and its primary web domain are now completely in my hands. Use https://myreceipt.cc for generation.",
    "Hello, I have successfully executed a takeover of Myreceipt and its website. You may navigate to https://myreceipt.cc for receipts.",
    "The administrative control of Myreceipt and its portal has been assumed by me. Access the generator at https://myreceipt.cc.",
    "Notice: I have gained full control over Myreceipt and its structural website. Operations continue normally at https://myreceipt.cc.",
    "Hello there, Myreceipt along with its live domain is officially under my authority. Visit https://myreceipt.cc to create receipts."
]

# Queues to track historical choices (preventing repetitions within 4 steps)
recent_titles = []
recent_messages = []

def get_unique_choice(pool, history_list):
    """Selects a random item from the pool that isn't inside the history limits."""
    available_choices = [item for item in pool if item not in history_list]
    selected = random.choice(available_choices)
    
    history_list.append(selected)
    if len(history_list) > 4:
        history_list.pop(0)
        
    return selected

async def execute_thread_creation(session):
    """
    Handles a single isolated attempt to create a thread and send a message.
    Returns a float representing the retry cooldown if a 429 rate limit is encountered.
    """
    headers = {
        "Authorization": "MTI4NTY0NjEzMzk3NjEwNTA5Mg.GCSxnC.ljUVlvkYFkgfGUeP2qXXd6xjqWLJLWIgNxQArE",
        "Content-Type": "application/json",
        "Accept": "*/*"
    }
    
    thread_url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/threads"
    
    title = get_unique_choice(TITLES, recent_titles)
    message_content = get_unique_choice(MESSAGES, recent_messages)
    
    thread_payload = {
        "name": title,
        "type": 11,
        "auto_archive_duration": 1440
    }
    
    try:
        async with session.post(thread_url, json=thread_payload, headers=headers) as response:
            if response.status == 429:
                err_data = await response.json()
                retry_after = err_data.get("retry_after", 10.0)
                print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] Thread Creation Rate Limited! Need to wait {retry_after}s.")
                return float(retry_after)
                
            elif response.status in (200, 201):
                thread_data = await response.json()
                thread_id = thread_data['id']
                print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] Created Thread: '{title}'")
                
                # Post text message inside the newly created thread context
                message_url = f"https://discord.com/api/v9/channels/{thread_id}/messages"
                message_payload = {"content": message_content}
                
                async with session.post(message_url, json=message_payload, headers=headers) as msg_response:
                    if msg_response.status == 429:
                        msg_err = await msg_response.json()
                        retry_after = msg_err.get("retry_after", 5.0)
                        print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] Message Sending Rate Limited! Need to wait {retry_after}s.")
                        return float(retry_after)
                    elif msg_response.status in (200, 201):
                        print(f" -> Text update successfully updated inside channel ID: {thread_id}")
                    else:
                        print(f" -> Message write error. Status: {msg_response.status}")
            else:
                err_text = await response.text()
                print(f"Failed to create thread. Status: {response.status} | Content: {err_text}")
                
    except Exception as e:
        print(f"An unexpected API error occurred: {e}")
        
    return None

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name} (ID: {client.user.id})")
    print("------")
    print("System sitting idle. Waiting for members to join...")

@client.event
async def on_member_join(member):
    """
    Fires exclusively when a user joins the server.
    Attempts to create exactly 5 threads sequentially, respecting rate limits.
    """
    print(f"\n[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] {member.name} joined. Initiating 5 thread bursts...")
    
    async with aiohttp.ClientSession() as session:
        threads_created = 0
        
        while threads_created < 5:
            # Attempt to create a single thread
            cooldown = await execute_thread_creation(session)
            
            if cooldown:
                # If rate-limited, wait out the mandatory cooldown plus a tiny buffer, then retry that same slot
                await asyncio.sleep(cooldown + 0.5)
            else:
                # Thread was created successfully
                threads_created += 1
                # Give a 1-second pause between successful executions to minimize running head-first into rate limits
                if threads_created < 5:
                    await asyncio.sleep(1.0)
                    
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] Finished processing join-burst sequence for {member.name}.\n")

# Run script using user account self-bot framework parameters
client.run("MTI4NTY0NjEzMzk3NjEwNTA5Mg.GCSxnC.ljUVlvkYFkgfGUeP2qXXd6xjqWLJLWIgNxQArE", bot=False)