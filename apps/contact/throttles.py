from rest_framework.throttling import AnonRateThrottle


class ContactRateThrottle(AnonRateThrottle):
    """
    Limits anonymous users to 5 contact-form submissions per hour.
    Override CONTACT_THROTTLE_RATE in settings to change.
    Rate string format: '<num>/<period>'  e.g. '5/hour', '3/min'
    """

    scope = "contact"
