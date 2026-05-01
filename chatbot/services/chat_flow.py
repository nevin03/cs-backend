import re
from chatbot.models import Lead

def handle_chat(session, message, extra_data=None):
    if extra_data is None:
        extra_data = {}
        
    step = session.step
    data = session.data
    message = message.strip() if message else ""
    
    # Handle direct bulk submission from frontend
    if message == "FINAL_LEAD_SUBMISSION":
        Lead.objects.create(
            name=extra_data.get("name", ""),
            phone=extra_data.get("contact", ""),
            place=extra_data.get("location", ""),
            interest=extra_data.get("services", "")
        )
        session.delete()
        return {
            "reply": "Thanks! We will contact you soon.",
            "step": "completed"
        }

    if step == "start":
        session.step = "interest"
        session.save()
        return {
            "reply": "Hey! What software are you looking for?",
            "options": ["Website", "Mobile App", "SaaS"],
            "step": "interest"
        }
        
    elif step == "interest":
        if not message:
            return {
                "reply": "Please select or type an interest.",
                "options": ["Website", "Mobile App", "SaaS"],
                "step": "interest"
            }
        data["interest"] = message
        session.step = "name"
        session.data = data
        session.save()
        return {
            "reply": "Great! Could you please tell me your name?",
            "step": "name"
        }
        
    elif step == "name":
        if not message:
            return {
                "reply": "Name cannot be empty. What is your name?",
                "step": "name"
            }
        data["name"] = message
        session.step = "phone"
        session.data = data
        session.save()
        return {
            "reply": f"Nice to meet you, {message}! What is your phone number?",
            "step": "phone"
        }
        
    elif step == "phone":
        cleaned_phone = message.replace(" ", "").replace("-", "")
        if not re.match(r'^\+?\d{9,15}$', cleaned_phone):
            return {
                "reply": "Please enter a valid phone number (e.g., +1234567890).",
                "step": "phone"
            }
        data["phone"] = message
        session.step = "place"
        session.data = data
        session.save()
        return {
            "reply": "Got it! Lastly, which city or place are you from?",
            "step": "place"
        }
        
    elif step == "place":
        if not message:
            return {
                "reply": "Place cannot be empty. Where are you from?",
                "step": "place"
            }
        data["place"] = message
        
        # Save Lead
        Lead.objects.create(
            name=data.get("name"),
            phone=data.get("phone"),
            place=data.get("place"),
            interest=data.get("interest")
        )
        
        # Reset Session or Delete
        session.delete()
        
        return {
            "reply": "Thanks! We will contact you soon.",
            "step": "completed"
        }
    
    # Fallback
    return {
        "reply": "Your session has already been completed.",
        "step": "completed"
    }
