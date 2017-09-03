##############################################################
# name: user_name
# type: function
# import by: ledger/views/transaction.py
#
# use:
##############################################################
# version author description                      date
# 1.0     awai   initial release                  23/07/2017
##############################################################

def user_name(request):
  
  from django.contrib.auth.models import User
  
  try:
    return User.objects.get(username=request.user.username).first_name
  except User.DoesNotExist:
    raise Exception(request.user.username + " is not having first name in database")
  except Exception as err:
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(err).__name__, err.args)
    raise Exception(err)