##############################################################
# name: device
# type: function
# import by: ledger/views/transaction.py
# use: 
##############################################################
# version author description                      date
# 1.0     awai   initial release                  23/07/2017
##############################################################

def device(request):
  
  try:
    if request.META.get('HTTP_USER_AGENT', '').lower().find("iphone") > 0:
      d = 'phone'
    else:
      d = 'others'
    return d
  except Exception as err:
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(err).__name__, err.args)
    raise Exception(err)