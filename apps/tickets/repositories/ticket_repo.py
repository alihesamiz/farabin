from apps.tickets.models import Ticket


class TicketRepository:
    @staticmethod
    def get_tickets_for_company(company):
        return Ticket.objects.select_related(
            "issuer",
        ).filter(issuer__company=company)
    
