from src.http_types.http_response import HttpResponse
from .errors_type.http_conflict import HttpConflictError
from .errors_type.http_not_found import HttpNotFound

def handle_error(error: Exception) -> HttpResponse:
    if isinstance(error, (HttpConflictError, HttpNotFound)):
        return HttpResponse(
            body={
                "errors": [{
                    "title": error.name,
                    "details": error.message
                }]
            },
            status_code=error.status_code
        )
    
    if isinstance(error, TypeError):
        title = "TypeError"
    else:
        title = "Error"
    return HttpResponse(
        body={
            "errors": [{
                "title": title,
                "details": str(error)
            }]
        }, 
        status_code=500   
    )