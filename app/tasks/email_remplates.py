from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings

def create_booking_confiramtion_template(
    booking: dict,
    email_to: EmailStr
):
    email = EmailMessage()

    email["Subject"] = "Booking Confrimation"
    email["From"] = settings.SMTP_USER
    email["to"] = email_to
    
    email.set_content(
        f"""
            <h1>Booking Confrimation<h1>
            You booked hotel {booking["date_from"]} to {booking["date_to"]}
        """,
        subtype="html"
    )
    return email