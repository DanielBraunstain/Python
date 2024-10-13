# error_handler.py
def handle_error(error_code):
    """
    handles error when getting data from weather server
    :param error_code: int indicating the error
    :return: error string
    """
    error_messages = {
        400: "Bad Request. wrong format.",
        401: "Unauthorized: invalid authentication.",
        404: "Not Found: location not found.",
        500: "Internal Server Error."
    }
    return error_messages.get(error_code, "An unexpected error occurred. Please try again later or contact support.")
